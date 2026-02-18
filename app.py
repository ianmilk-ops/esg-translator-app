import streamlit as st
import google.generativeai as genai

# 1. 安全配置：從 Streamlit Secrets 讀取金鑰
# 部署後，請記得在 Streamlit Cloud 後台設定 GEMINI_API_KEY
# --- 修正後的初始化段落 ---
if "GEMINI_API_KEY" in st.secrets:
    # 1. 配置金鑰
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # 2. 強制指定模型，若 gemini-1.5-flash 報錯，則改用 gemini-pro 作為備援
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # 測試連線，若這行失敗會跳到 except
        model.generate_content("test") 
    except:
        # 備援方案：使用最穩定的 gemini-pro 名稱
        model = genai.GenerativeModel('gemini-pro')
else:
    st.error("請在 Streamlit Secrets 中設定 GEMINI_API_KEY")
# -------------------------

# 2. 定義「務實派顧問」的指令
SYSTEM_PROMPT = """
你是一位務實的「節能減碳與融資顧問」。
當使用者輸入內容時，請執行：
1. 精準翻譯：將原文翻譯成專業且易懂的繁體中文。
2. 經濟效益分析：若內容涉及儲能 (ESS)、微電網 (Microgrid) 或節能設備，
   請標註該項目如何協助對接「綠色貸款」或「永續連結貸款 (SLL)」。
3. 務實口吻：強調利息減免與回收期，語氣乾脆，直接切入供應鏈優勢。
"""

# 3. 介面設定
st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")
st.title("🚜 務實派 ESG 顧問翻譯助手")
st.markdown("---")

source_text = st.text_area("請輸入英文原文：", placeholder="例如：Installing an Energy Storage System...")

if st.button("生成專業翻譯與建議"):
    if source_text:
        with st.spinner("顧問正在分析供應鏈與融資潛力..."):
            try:
                full_prompt = f"{SYSTEM_PROMPT}\n\n待處理文字：\n{source_text}"
                response = model.generate_content(full_prompt)
                
                st.subheader("📝 翻譯與顧問建議")
                st.info(response.text)
            except Exception as e:
                st.error(f"發生錯誤：{e}")
    else:
        st.warning("請輸入內容後再點擊按鈕。")
      
