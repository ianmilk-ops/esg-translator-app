import streamlit as st
from google import genai

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 取得 Client
def get_client():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ 請在 Secrets 中設定 GEMINI_API_KEY")
        return None
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"], http_options={'api_version': 'v1'})

client = get_client()

# 2. 模型選擇（萬一 1.5-flash 不行，你可以手動換 2.0-flash 或 pro）
model_option = st.selectbox(
    "選擇模型版本：",
    ["gemini-1.5-flash", "gemini-2.0-flash", "gemini-1.5-pro", "gemini-pro"],
    index=0
)

# 3. 顧問指令
SYSTEM_PROMPT = """你是一位專業的節能減碳顧問。
1. 精準翻譯原文為繁體中文。
2. 若涉及儲能、節能、電力系統，請標註該項目在台灣對接「綠色貸款」或「節能補助」的潛力。"""

source_text = st.text_area("請輸入英文原文：", height=150, placeholder="例如：The ESS deployment enhances grid stability...")

if st.button("🚀 開始分析"):
    if client and source_text:
        with st.spinner("分析中..."):
            try:
                # 執行生成
                response = client.models.generate_content(
                    model=model_option,
                    contents=f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"分析失敗。請嘗試更換模型版本或檢查金鑰。錯誤細節：{e}")

st.caption("v2026.02.18 | 專為節能顧問打造的行動翻譯工具")
