import streamlit as st
from google import genai

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 取得 Client (強制指定 API 版本)
@st.cache_resource
def get_client():
    if "GEMINI_API_KEY" not in st.secrets:
        return None
    # 強制鎖定正式版通道
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"], 
        http_options={'api_version': 'v1'}
    )

client = get_client()

# 2. 定義顧問指令 (這部分融合了您的專業背景)
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
1. 將英文原文精準翻譯為專業繁體中文。
2. 針對儲能、節能改善、電力系統等內容，標註對應「綠色融資」或「節能補助」的潛力。
3. 語氣乾脆、專業。"""

# 3. 介面與生成邏輯
source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("🚀 開始分析並生成建議"):
    if not client:
        st.error("❌ Secrets 中未偵測到 API Key，請檢查設定。")
    elif not source_text:
        st.warning("請輸入內容再點擊。")
    else:
        with st.spinner("顧問正在透過 Gemini 1.5 正式版進行分析..."):
            try:
                # 這裡直接「寫死」模型名稱，避開找不到屬性的問題
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                # 若 1.5 不行，最後一個機會是最新版本的 2.0
                try:
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                    )
                    st.info(response.text)
                except Exception as e2:
                    st.error(f"連線失敗。請檢查 Google AI Studio 權限。錯誤細節：{e2}")
