import streamlit as st
import google.generativeai as genai
import os

# 1. 頁面基本設定
st.set_page_config(page_title="ESG 顧問翻譯助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手 (診斷版)")

# 2. 初始化
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 未偵測到 API Key！請在 Streamlit Cloud 的 Secrets 設定 'GEMINI_API_KEY'。")
    st.stop()

# 設定 API Key
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 定義 Prompt
SYSTEM_PROMPT = """你是一位專業的「節能減碳顧問團隊主管」。
你的任務是將英文原文精準翻譯為專業繁體中文。"""

# 4. 介面
source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("🚀 生成翻譯"):
    if not source_text:
        st.warning("請輸入內容。")
    else:
        with st.spinner("連線分析中..."):
            try:
                # --- 嘗試 A：標準 1.5 Flash ---
                st.info("正在嘗試連接 gemini-1.5-flash...")
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n{source_text}")
                st.success("成功連接 gemini-1.5-flash！")
                st.markdown(response.text)

            except Exception as e:
                # --- 錯誤處理：列出可用模型 ---
                st.error(f"❌ 模型連接失敗：{e}")
                st.warning("⚠️ 系統正在自動檢測您的 API Key 可用的模型列表...")
                
                try:
                    # 列出所有可用的模型
                    available_models = []
                    for m in genai.list_models():
                        if 'generateContent' in m.supported_generation_methods:
                            available_models.append(m.name)
                    
                    st.write("### ✅ 您的 API Key 實際可用的模型如下：")
                    st.code("\n".join(available_models))
                    st.write("請將上列其中一個名稱 (例如 models/gemini-pro) 告訴我，或直接修改程式碼中的 model 名稱。")
                    
                except Exception as list_error:
                    st.error(f"連模型列表都無法讀取，可能是 API Key 無效或網路問題：{list_error}")

st.caption("v2026.02.18 | 診斷模式")
