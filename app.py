import streamlit as st
from google import genai

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

@st.cache_resource
def get_ready_model():
    if "GEMINI_API_KEY" not in st.secrets:
        return None, "請先設定 Secrets"
    
    try:
        # 使用最新 v1 API 版本
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"], http_options={'api_version': 'v1'})
        
        # 2026 最新推薦：直接測試這兩個名稱，這在目前免費通道最容易通
        for name in ['gemini-2.0-flash', 'gemini-1.5-flash', 'gemini-2.0-flash-exp']:
            try:
                # 測試生成
                client.models.generate_content(model=name, contents="test")
                return client, name
            except:
                continue
        return None, "找不到可用模型，請確認 API Key 權限"
    except Exception as e:
        return None, str(e)

client, model_name = get_ready_model()

# 狀態與功能介面
if client:
    st.success(f"✅ 顧問已連線 (使用模型: {model_name})")
    
    source_text = st.text_area("請輸入英文原文：", height=150)
    if st.button("🚀 開始分析"):
        with st.spinner("分析中..."):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"你是一位節能減碳顧問。請精準翻譯為繁體中文，並提供節能改善與融資建議：\n\n{source_text}"
                )
                st.info(response.text)
            except Exception as e:
                st.error(f"生成失敗：{e}")
else:
    st.error(f"❌ 連線失敗：{model_name}")
