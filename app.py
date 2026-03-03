import streamlit as st
from langchain_groq import ChatGroq

# --- 1. إعداد الواجهة ---
st.set_page_config(page_title="المساعد الذكي الآمن", page_icon="🚀", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [data-testid="stSidebar"], .stMarkdown, .stChatMessage {
        direction: rtl; text-align: right; font-family: 'Cairo', sans-serif;
    }
    .stChatMessage { border-radius: 15px; margin: 10px 0; border: 1px solid #00ffa3; }
    </style>
    """, unsafe_allow_html=True)

st.title("🚀 المساعد الذكي (النسخة السحابية الآمنة)")

# --- 2. سحب المفتاح المخفي ---
# هنا قمنا بتغيير الكود ليقرأ المفتاح من إعدادات الموقع السرية (Secrets)
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
except KeyError:
    st.error("لم يتم العثور على مفتاح API. تأكد من إضافته في إعدادات Secrets في Streamlit Cloud.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

try:
    # استخدام الموديل المستقر
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.3-70b-versatile",
        temperature=0.7
    )

    # عرض الرسائل
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # استقبال السؤال
    if prompt := st.chat_input("تحدث معي الآن، أنا أعمل بالسحاب..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            res_placeholder = st.empty()
            full_res = ""
            
            try:
                response = llm.stream(prompt)
                for chunk in response:
                    full_res += chunk.content
                    res_placeholder.markdown(full_res + "▌")
                
                res_placeholder.markdown(full_res)
                st.session_state.messages.append({"role": "assistant", "content": full_res})
            except Exception as e:
                st.error("خطأ في الاتصال بالموديل السحابي.")

except Exception as e:
    st.error(f"خطأ في التهيئة: {e}")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    st.info("الموديل: Llama 70B (Cloud)")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()