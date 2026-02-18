import streamlit as st
from google import genai
from google.genai import types

# 1. 頁面基本設定
st.set_page_config(page_title="ESG 顧問翻譯助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 2. 初始化 API 連線
@st.cache_resource
def init_client():
    # 檢查是否設定了 API Key
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ 未偵測到 API Key！請在 Streamlit Cloud 的 Secrets 設定 'GEMINI_API_KEY'。")
        st.stop()
    
    # 初始化 Client (使用新版 SDK 寫法)
    # 移除 http_options 強制設定，讓 SDK 自動選擇最佳路徑
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

client = init_client()

# 3. 定義顧問核心指令
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
你的任務是將英文原文精準翻譯為專業繁體中文。
特別針對以下議題提供見解：永續經營、ESG、能源管理、碳盤查、節能改善方案(空調、電力、儲能等)、綠建築標章。
若內容涉及技術改善，請標註對應「綠色融資」或「政府補助」的潛力。"""

# 4. 介面與生成邏輯
source_text = st.text_area("請輸入英文原文 (例如 ESG 報告或技術文件)：", height=150)

if st.button("🚀 生成專業翻譯與建議"):
    if not source_text:
        st.warning("請輸入內容。")
    else:
        with st.spinner("顧問分析中..."):
            try:
                # 設定生成參數 (可選，這裡設定溫度讓回答更穩定)
                config = types.GenerateContentConfig(
                    temperature=0.3, # 翻譯建議數值低一點較精準
                )

                # 呼叫 API
                # 使用目前最穩定的免費模型 gemini-1.5-flash
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}",
                    config=config
                )
                
                # 顯示結果
                st.subheader("📝 翻譯與建議")
                if response.text:
                    st.success("分析完成！")
                    st.markdown(response.text)
                else:
                    st.warning("模型回應為空，請稍後再試。")

            except Exception as e:
                # 這裡會顯示真正的錯誤原因，而不是被 2.0 的錯誤覆蓋
                st.error(f"發生錯誤，請檢查以下訊息：\n{e}")
                
st.caption("v2026.02.18 | 專為節能減碳顧問量身打造")
