import streamlit as st
import google.generativeai as genai
from PIL import Image
import io

# 1. API Tənzimləməsi
# Secrets-dən oxumağa çalışır, yoxdursa koddan oxuyur
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
except:
    api_key = "SƏNİN_API_AÇARIN_BURA"

genai.configure(api_key=api_key)

# 2. Səhifə Ayarları
st.set_page_config(page_title="Perfect AI", page_icon="🌟")
st.title("🌟 Perfect AI")

# Yaddaş (History) funksiyası
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 3. Modelin Başladılması (Stabil versiya)
model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="Sənin adın 'Perfect AI'-dir. Mehriban köməkçi ol. Birbaşa cavab ver."
)

# 4. İnterfeys Elementləri
col1, col2 = st.columns([3, 1])
with col2:
    if st.button("Yaddaşı Sil"):
        st.session_state.chat_history = []
        st.rerun()

# Şəkil yükləmə bölməsi
uploaded_file = st.file_uploader("Şəkil seçin (isteğe bağlı)...", type=["jpg", "jpeg", "png"])

# 5. Söhbət Tarixçəsini Göstər
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. İstifadəçi Girişi və Cavab
if prompt := st.chat_input("Mesajınızı yazın..."):
    # İstifadəçi mesajını göstər
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Botun cavabı
    with st.chat_message("assistant"):
        with st.spinner("Düşünürəm..."):
            try:
                if uploaded_file:
                    # Şəkilli cavab
                    img = Image.open(uploaded_file)
                    response = model.generate_content([prompt, img])
                else:
                    # Sadəcə mətn
                    chat = model.start_chat(history=[{"role": m["role"], "parts": [m["content"]]} for m in st.session_state.chat_history[:-1]])
                    response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.chat_history.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Xəta baş verdi: {e}")

