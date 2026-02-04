import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. API Tənzimləməsi
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# 2. Səhifə Tənzimləmələri
st.set_page_config(page_title="Perfect AI", page_icon="🌟")
st.title("🌟 Perfect AI")

# Yaddaş (History) funksiyası üçün session_state yaradırıq
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Modelin başladılması
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="Sənin adın 'Perfect AI'-dir. İstifadəçi hansı dildə yazırsa, "
                       "sən də o dildə 'Salam! Necəsən, sizə necə kömək edə bilərəm?' "
                       "deyərək söhbətə başla. Söhbət tarixçəsini daimi yadda saxla."
)

# 3. Söhbət Tarixçəsini Göstər
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. Giriş Hissəsi (Mətn və Şəkil)
prompt = st.chat_input("Mesajınızı yazın...")
uploaded_file = st.sidebar.file_uploader("Şəkil yüklə", type=["jpg", "jpeg", "png"])

if prompt or uploaded_file:
    # İstifadəçinin mesajını göstər
    with st.chat_message("user"):
        if prompt: st.markdown(prompt)
        if uploaded_file: st.image(uploaded_file, caption="Yüklənən şəkil")

    # AI Cavabı
    with st.chat_message("assistant"):
        try:
            # Şəkil varsa, həm şəkil həm mətni göndər
            content = []
            if prompt: content.append(prompt)
            if uploaded_file:
                img = Image.open(uploaded_file)
                content.append(img)
            
            response = model.generate_content(content)
            st.markdown(response.text)
            
            # Tarixçəyə əlavə et
            st.session_state.chat_history.append({"role": "user", "content": prompt if prompt else "Şəkil göndərildi"})
            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            
        except Exception as e:

            st.error(f"Xəta: {e}")
