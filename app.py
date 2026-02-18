import streamlit as st
from google import genai

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 建立 Client
@st.cache_resource
def setup_ai():
    if "GEMINI_API_KEY" not in st.secrets:
        return None, None, "請在 Secrets 中設定 GEMINI_API_KEY"
    
    try:
        # 建立連線
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"], http_options={'api_version': 'v1'})
        
        # 動態列出所有支援生成內容的模型
        # 注意：我們使用最保險的方式獲取模型清單
        model_list = []
        for m in client.models.list():
            # 2026 最新 SDK 屬性檢查
            model_list.append(m.name)
        
        if not model_list:
            return None, None, "帳號下無可用模型"
     # 優先選擇 1.5-flash，因為它的免費額度最穩
        target = next((m for m in model_list if '1.5-flash' in m), 
                      next((m for m in model_list if '2.0-flash' in m), model_list[0]))       
        # 優先順序：2.0-flash > 1.5-flash > 第一個可用的
        target = next((m for m in model_list if '2.0-flash' in m), 
                      next((m for m in model_list if '1.5-flash' in m), model_list[0]))
        
        return client, target, "✅ 顧問連線成功"
    except Exception as e:
        return None, None, f"連線異常：{str(e)}"

client, model_name, status_msg = setup_ai()

# 2. 顯示狀態
if client:
    st.success(f"{status_msg} (使用模型: {model_name})")
else:
    st.error(status_msg)

# 3. 顧問功能
SYSTEM_PROMPT = "你是一位務實的節能減碳顧問。請精準翻譯原文為繁體中文，並針對儲能、節能改善等項目提供綠色貸款與供應鏈競爭力建議。"

source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("🚀 開始分析"):
    if client and source_text:
        with st.spinner("分析中..."):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"生成失敗。錯誤細節：{e}")
