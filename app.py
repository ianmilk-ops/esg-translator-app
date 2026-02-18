import streamlit as st
import google.generativeai as genai
import os

# 1. 頁面基本設定 (針對手機螢幕優化)
st.set_page_config(
    page_title="ESG 顧問助手 v3.0", 
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定義 CSS 讓手機顯示更美觀
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        padding: 8px 16px; 
        background-color: #f0f2f6; 
        border-radius: 10px 10px 0px 0px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🚜 務實派 ESG 顧問助手 (v3.0 手機優化版)")

# 2. 初始化與設定 API Key
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 未偵測到 API Key！請在 Streamlit Cloud 的 Secrets 設定 'GEMINI_API_KEY'。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 定義顧問核心指令 (已優化手機閱讀格式)
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
請將英文原文翻譯為專業繁體中文，並嚴格遵守以下「移動端優化」格式輸出：

1. **🚀 核心摘要**：用 3 點 bullet points 說明原文最重要訊息。
2. **📖 專業翻譯**：使用精確的產業術語（如：碳定價、範疇三、熱泵效率、儲能、綠建築標章等）。
3. **💡 顧問洞察**：
   - ⚡️ **技術與法規面**：標註改善工程關鍵或法規遵循建議。
   - 🏦 **資金與補助面**：條列對應的「政府補助」或「綠色融資」潛力。

請多利用 **粗體** 與符號方便手機掃視。"""

# 4. 介面與生成邏輯
with st.expander("📌 查看顧問設定指令", expanded=False):
    st.caption(SYSTEM_PROMPT)

source_text = st.text_area("請輸入英文原文 (ESG 報告或技術文件)：", height=200, placeholder="在此貼上內容...")

if st.button("🚀 生成專業翻譯與建議"):
    if not source_text:
        st.warning("請輸入內容。")
    else:
        # 使用 status 讓載入過程在手機上更有動感
        with st.status("🔍 顧問團隊分析中...", expanded=True) as status:
            try:
                # 使用最新的 Flash 模型
                model = genai.GenerativeModel('gemini-2.0-flash') 
                
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}",
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3
                    )
                )
                
                status.update(label="✅ 分析完成！", state="complete", expanded=False)

                # 5. 輸出結果 (使用分頁標籤優化手機閱讀)
                st.subheader("📝 顧問分析報告")
                
                # 簡單拆分內容（如果 AI 有按格式輸出）
                res_text = response.text
                
                tab1, tab2 = st.tabs(["📄 專業翻譯與摘要", "💡 顧問建議與資金"])
                
                with tab1:
                    st.markdown(res_text)
                
                with tab2:
                    st.success("💰 針對此項目的實務建議")
                    if "補助" in res_text or "融資" in res_text:
                        st.info("💡 提醒：系統偵測到此項目具備申請政府補助或綠色貸款的潛力。")
                    else:
                        st.write("建議諮詢專業工程團隊進行節能績效 (ESCO) 評估。")

            except Exception as e:
                status.update(label="❌ 發生錯誤", state="error")
                st.error(f"錯誤訊息：{e}")

st.caption("v2026.02.19 | 移動端優化介面 | Powered by Gemini 2.0 Flash")
