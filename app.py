import streamlit as st
from google import genai

# 頁面設定
st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 初始化最新版 Client
@st.cache_resource
def get_client():
    if "GEMINI_API_KEY" in st.secrets:
        return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    return None

client = get_client()

if not client:
    st.error("❌ 請在 Secrets 中設定 GEMINI_API_KEY")

# 2. 顧問指令
SYSTEM_PROMPT = "你是一位務實的節能減碳顧問。請精準翻譯以下內容為繁體中文，並針對儲能、節能改善等項目提供綠色貸款與供應鏈競爭力建議。"

# 3. 介面
source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("生成專業建議"):
    if source_text and client:
        with st.spinner("最新版 Gemini 正在分析中..."):
            try:
                # 使用最新版 SDK 呼叫方式
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"分析失敗，請檢查金鑰或權限。錯誤細節：{e}")
