import streamlit as st
import google.generativeai as genai

# 1. 頁面基本設定 (放在最前面)
st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")

# 2. 初始化 API 金鑰
def init_gemini():
    if "GEMINI_API_KEY" in st.secrets:
        try:
            genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
            # 直接指定最新穩定的模型
            return genai.GenerativeModel('gemini-1.5-flash')
        except Exception as e:
            st.error(f"API 設定失敗: {e}")
    else:
        st.error("請在 Streamlit Secrets 中設定 GEMINI_API_KEY")
    return None

model = init_gemini()

# 3. 介面與功能
st.title("🚜 務實派 ESG 顧問翻譯助手")
st.markdown("---")

# 定義顧問指令
SYSTEM_PROMPT = """你是一位務實的「節能減碳與融資顧問」。
1. 將原文精準翻譯成專業繁體中文。
2. 若涉及能源基建（儲能、節能、光電），標註其對「綠色融資」的幫助。
3. 語氣乾脆、務實。"""

# 輸入框（加上 key 以確保狀態穩定）
source_text = st.text_area("請輸入英文原文：", height=150, key="input_text")

if st.button("生成專業翻譯與建議", key="submit_button"):
    if not source_text:
        st.warning("請輸入內容。")
    elif not model:
        st.error("模型未就緒，請檢查 Secrets 設定。")
    else:
        with st.spinner("顧問正在分析中..."):
            try:
                # 執行生成
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n內容：{source_text}")
                st.subheader("📝 翻譯與顧問建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"分析失敗，請稍後再試。錯誤細節: {e}")

# 4. 底部備註
st.caption("powered by Gemini 1.5 Flash | 專為節能顧問打造")
