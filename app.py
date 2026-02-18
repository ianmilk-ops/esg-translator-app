import streamlit as st
import google.generativeai as genai
import os

# 1. 頁面基本設定
st.set_page_config(
    page_title="ESG 顧問專業版 v3.5", 
    page_icon="💎",
    layout="centered"
)

# 2. API 設定與初始化
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 未偵測到 API Key！請在 Streamlit Cloud 設定中配置。")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 系統核心指令
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
你的任務是將英文原文精準翻譯為專業繁體中文，並針對以下維度進行深度分析：
1. **🚀 核心摘要**：3點精煉內容。
2. **📖 專業譯文**：確保術語符合台灣產業習慣（如：能源效率、負載、綠電媒合）。
3. **💡 顧問洞察**：
   - ⚡️ **技術改善**：對應空調、儲能、電力系統等具體方案。
   - 🏦 **資金來源**：明確指出適用之「政府補助」或「綠色金融」潛力。
請使用表格與粗體字體優化手機閱讀體驗。"""

# 4. 介面呈現
st.title("🛡️ ESG 顧問專業版 (v3.5)")
st.caption("目前運行模型：Gemini 2.5 Flash (高配額模式)")

source_text = st.text_area("請貼上 ESG 報告或技術文件：", height=200)

if st.button("🚀 執行深度分析"):
    if not source_text:
        st.warning("內容不可為空。")
    else:
        with st.status("💎 正在調用高階模型進行分析...", expanded=True) as status:
            try:
                # 使用您指定的 Gemini 2.5 Flash
                model = genai.GenerativeModel('gemini-2.5-flash')
                
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}",
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3
                    )
                )
                
                # 顯示結果
                status.update(label="✅ 分析完成", state="complete", expanded=False)
                
                st.subheader("📝 分析報告")
                tab1, tab2 = st.tabs(["📄 專業翻譯", "🔍 補助與改善建議"])
                
                with tab1:
                    st.markdown(response.text)
                
                with tab2:
                    # 這裡可以額外放一些針對顧問主管的 SOP 提醒
                    st.success("💰 資金規劃建議")
                    st.info("若此項目涉及設備汰換，請確認是否符合『經濟部商業司節能設備補助』。")

            except Exception as e:
                error_msg = str(e)
                status.update(label="❌ 呼叫失敗", state="error")
                if "429" in error_msg:
                    st.error("⚠️ **配額受限 (Quota Exceeded)**")
                    st.markdown("""
                    **解決方案：**
                    1. 進入 [Google AI Studio](https://aistudio.google.com/)。
                    2. 檢查左側的 **Plan & Billing**。
                    3. 確認是否已將您的 Project 從 **Free Tier** 切換至 **Pay-as-you-go**。
                    *註：個人 Gemini Advanced 訂閱不等於 API 的付費配額，需分開設定。*
                    """)
                else:
                    st.error(f"發生非預期錯誤：{error_msg}")

st.divider()
st.caption("© 2026 ESG 顧問團隊主管專用版 | 穩定性優化中")
