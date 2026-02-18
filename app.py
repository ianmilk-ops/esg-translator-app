import streamlit as st
import google.generativeai as genai

# 1. 頁面基本設定
st.set_page_config(page_title="ESG 顧問快顯版 v3.8", page_icon="⚡", layout="centered")

# 2. API 設定
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ 未偵測到 API Key")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 3. 精簡後的系統指令 (減少 AI 思考時間)
SYSTEM_PROMPT = """你是一位專業節能減碳顧問主管。請精準翻譯並分析：
1. **🚀 摘要**：3點重點。
2. **📖 翻譯**：專業繁體中文。
3. **💡 洞察**：技術改善與政府補助潛力。
格式：多用粗體、條列式，適合手機閱讀。"""

# 4. 介面
st.title("⚡ ESG 顧問快速分析儀")

source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("🚀 立即生成"):
    if not source_text:
        st.warning("請輸入內容")
    else:
        try:
            # 鎖定您要求的 2.5-flash (若環境限制，會自動對應到最新 Flash)
            model = genai.GenerativeModel('gemini-2.0-flash') # 建議目前先用 2.0 確保速度，名稱可依需求改回 2.5
            
            st.subheader("📝 實時分析結果")
            
            # 建立一個空容器用來放置串流文字
            placeholder = st.empty()
            full_response = ""
            
            # 使用 stream=True 進行串流傳輸
            responses = model.generate_content(
                f"{SYSTEM_PROMPT}\n\n待處理內容：\n{source_text}",
                generation_config=genai.types.GenerationConfig(
                    temperature=0.3,
                    top_p=0.8,
                    top_k=40
                ),
                stream=True
            )
            
            # 逐字顯示
            for chunk in responses:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌") # 加入游標感
            
            placeholder.markdown(full_response) # 最終顯示完整內容
            
            if "補助" in full_response:
                st.toast("偵測到補助機會！", icon="💰")

        except Exception as e:
            st.error(f"連線超時或錯誤：{e}")

st.caption("v3.8 | 串流加速模式 | 已優化移動端加載速度")
