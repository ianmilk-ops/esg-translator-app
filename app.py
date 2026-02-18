import streamlit as st
from google import genai

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 初始化 Client
@st.cache_resource
def get_ready_model():
    if "GEMINI_API_KEY" not in st.secrets:
        return None, "請設定 Secrets"
    
    try:
        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"], http_options={'api_version': 'v1'})
        
        # 關鍵：自動列出你帳號下所有可用的模型
        available_models = [m.name for m in client.models.list() if 'generateContent' in m.supported_methods]
        
        if not available_models:
            return None, "找不到可用模型"
            
        # 優先選擇 flash 或 pro，否則選第一個
        target = next((m for m in available_models if 'flash' in m), available_models[0])
        return client, target
    except Exception as e:
        return None, str(e)

client, model_name = get_ready_model()

# 2. 狀態顯示
if client:
    st.success(f"✅ 連線成功！使用模型：{model_name}")
else:
    st.error(f"❌ 連線失敗：{model_name}")

# 3. 顧問功能
SYSTEM_PROMPT = "你是一位務實的節能減碳顧問。請精準翻譯以下內容為繁體中文，並提供節能改善建議。"

source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("生成專業建議"):
    if source_text and client:
        with st.spinner("分析中..."):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                )
                st.info(response.text)
            except Exception as e:
                st.error(f"生成失敗：{e}")
