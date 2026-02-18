import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

st.set_page_config(page_title="ESG 顧問助手", page_icon="💰")

# 1. 初始化與強制路徑設定
def get_model():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("請在 Secrets 設定 GEMINI_API_KEY")
        return None
    
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)

    # 這裡列出所有可能的名稱組合，總有一個會中
    model_candidates = ['gemini-1.5-flash', 'models/gemini-1.5-flash', 'gemini-pro']
    
    for model_name in model_candidates:
        try:
            # 強制指定 API 版本為 v1 (正式版) 避開 v1beta 錯誤
            model = genai.GenerativeModel(model_name=model_name)
            # 測試連線
            model.generate_content("test", request_options=RequestOptions(api_version='v1'))
            return model, model_name
        except:
            try:
                # 若 v1 不行，嘗試預設路徑
                model = genai.GenerativeModel(model_name=model_name)
                model.generate_content("test")
                return model, model_name
            except:
                continue
    return None, None

model, final_name = get_model()

# 2. 介面設計
st.title("🚜 務實派 ESG 顧問翻譯助手")
st.markdown(f"**目前狀態：** {'✅ 顧問已連線 (' + final_name + ')' if model else '❌ 連線失敗'}")

SYSTEM_PROMPT = "你是一位務實的節能減碳與融資顧問。請精準翻譯以下內容為繁體中文，並針對儲能、節能改善等項目提供綠色貸款相關建議。"

source_text = st.text_area("請輸入英文原文：", height=150)

if st.button("生成專業建議"):
    if source_text and model:
        with st.spinner("正在穿越網際網路獲取建議..."):
            try:
                # 再次確保使用 v1 版本呼叫
                response = model.generate_content(
                    f"{SYSTEM_PROMPT}\n\n內容：{source_text}",
                    request_options=RequestOptions(api_version='v1')
                )
                st.info(response.text)
            except Exception as e:
                st.error(f"分析失敗，錯誤代碼：{e}")
