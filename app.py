import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 強制指定 v1 正式版通道
@st.cache_resource
def get_client():
    if "GEMINI_API_KEY" in st.secrets:
        # 關鍵點：在此加入 http_options 來強制鎖定 API 版本
        return genai.Client(
            api_key=st.secrets["GEMINI_API_KEY"],
            http_options={'api_version': 'v1'} 
        )
    return None

client = get_client()

# 2. 顧問指令
SYSTEM_PROMPT = "你是一位務實的節能減碳顧問。請精準翻譯以下內容為繁體中文，並針對儲能、節能改善等項目提供建議。"

# 3. 介面
source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("生成專業建議"):
    if source_text and client:
        with st.spinner("強制 v1 通道分析中..."):
            try:
                # 執行生成
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                # 如果 1.5-flash 還是不行，嘗試備援模型名稱
                try:
                    response = client.models.generate_content(
                        model='gemini-2.0-flash', # 試試看最新的 2.0
                        contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                    )
                    st.info(response.text)
                except:
                    st.error(f"分析失敗。技術細節：{e}")
