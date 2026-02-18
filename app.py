import streamlit as st
from google import genai

# 1. 頁面基本設定
st.set_page_config(page_title="ESG 顧問翻譯助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 2. 初始化 API 連線
@st.cache_resource
def init_client():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ 請在 Streamlit Cloud 的 Secrets 中設定 GEMINI_API_KEY")
        return None
    # 強制鎖定正式版 API 通道
    return genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"],
        http_options={'api_version': 'v1'}
    )

client = init_client()

# 3. 定義顧問核心指令 (結合您的專業背景)
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
你的任務是將英文原文精準翻譯為專業繁體中文。
特別針對以下議題提供見解：永續經營、ESG、能源管理、碳盤查、節能改善方案(空調、電力、儲能等)、綠建築標章。
若內容涉及技術改善，請標註對應「綠色融資」或「政府補助」的潛力。"""

# 4. 介面與生成邏輯
source_text = st.text_area("請輸入英文原文 (例如 ESG 報告或技術文件)：", height=150)

if st.button("🚀 生成專業翻譯與建議"):
    if not source_text:
        st.warning("請輸入內容。")
    elif not client:
        st.error("API 未就緒。")
    else:
        with st.spinner("顧問分析中..."):
            try:
                # 直接鎖定最穩定的 gemini-1.5-flash 模型
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}"
                )
                st.subheader("📝 翻譯與建議")
                st.info(response.text)
            except Exception as e:
                # 備援邏輯：若 1.5 版有問題，嘗試 2.0 版
                try:
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=f"{SYSTEM_PROMPT}\n\n內容：{source_text}"
                    )
                    st.info(response.text)
                except Exception as e2:
                    st.error(f"目前 API 配額受限，請稍後再試。錯誤細節：{e2}")

st.caption("v2026.02.18 | 專為節能減碳顧問量身打造")
