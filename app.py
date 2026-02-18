import streamlit as st
import google.generativeai as genai
import os

# 1. 頁面基本設定
st.set_page_config(page_title="ESG 顧問翻譯助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手 (v2.5版)")

# 2. 初始化與設定 API Key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 未偵測到 API Key！請在 Streamlit Cloud 的 Secrets 設定 'GEMINI_API_KEY'。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

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
        with st.spinner("顧問分析中 (使用 Gemini 2.5)..."):
            try:
                # -------------------------------------------------------
                # 關鍵修改：使用您列表中的 'gemini-2.5-flash'
                # 這是您帳號目前最強且快速的模型
                # -------------------------------------------------------
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                # 發送請求
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}",
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3  # 降低隨機性
                    )
                )
                
                # 顯示結果
                st.subheader("📝 翻譯與建議")
                if response.text:
                    st.success("分析完成！")
                    st.markdown(response.text)
                else:
                    st.warning("模型回應為空，請稍後再試。")

            except Exception as e:
                # 如果 2.5-flash 也被限制額度，這裡會顯示錯誤
                st.error(f"發生錯誤：{e}")
                st.info("建議：如果顯示 Quota/Limit 錯誤，請嘗試改用 'gemini-flash-lite-latest'")
                
st.caption("v2026.02.18 | Powered by Gemini 2.5")
