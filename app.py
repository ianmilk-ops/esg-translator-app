import streamlit as st
import google.generativeai as genai

# 設定頁面
st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")

# 1. 從 Secrets 讀取金鑰
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # --- 自動模型偵測邏輯 ---
    # 我們依序測試這些可能的模型名稱
    model_names = ['gemini-1.5-flash', 'gemini-1.5-pro', 'gemini-pro']
    model = None
    
    for name in model_names:
        try:
            temp_model = genai.GenerativeModel(name)
            # 進行極短的測試連線
            temp_model.generate_content("hi", generation_config={"max_output_tokens": 1})
            model = temp_model
            break # 成功找到可用的模型，跳出迴圈
        except:
            continue
            
    if model is None:
        st.error("目前無法連接到 Gemini 模型，請檢查 API Key 是否有效。")
else:
    st.error("請在 Streamlit Secrets 中設定 GEMINI_API_KEY")

# 2. 顧問指令
SYSTEM_PROMPT = """你是一位務實的「節能減碳與融資顧問」。
1. 將原文精準翻譯成專業繁體中文。
2. 若涉及能源基建，提供「綠色融資」與「供應鏈門票」建議。
3. 語氣乾脆、務實。"""

# 3. 介面
source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("生成專業翻譯與建議"):
    if source_text and model:
        with st.spinner("顧問正在分析中..."):
            try:
                response = model.generate_content(f"{SYSTEM_PROMPT}\n\n內容：{source_text}")
                st.subheader("📝 翻譯與顧問建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"連線成功但生成失敗：{e}")
