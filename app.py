import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Tənzimləməsi (Secrets-dən oxuyur)
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Səhifə Tənzimləmələri
st.set_page_config(page_title="Perfect AI", page_icon="🌟")
st.title("🌟 Perfect AI")

# Yaddaş (History) funksiyası
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Modelin başladılması
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    system_instruction="Sənin adın 'Perfect AI'-dir. İstifadəçi ilə mehriban və köməkçi tonda danış. Hər mesajda salam vermə, birbaşa sualları cavablandır."
)

# Sohbet tarixçəsini göstər
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# İstifadəçi girişi
if prompt := st.chat_input("Mesajınızı yazın..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat = model.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.chat_history[:-1]])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
