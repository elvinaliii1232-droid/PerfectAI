import google.generativeai as genai
from IPython.display import display, Markdown, clear_output
import ipywidgets as widgets
from PIL import Image
import io

# 1. API tənzimləmələri
genai.configure(api_key="AIzaSyAbkgdf-7JhEJFC-DF0g1OWpJ57zo5DpJU")

# Yaddaş (History) üçün siyahı yaradırıq
if 'chat_history' not in globals():
    chat_history = []

model = genai.GenerativeModel(
    model_name='gemini-2.0-flash',
    system_instruction="Sənin adın 'Perfect AI'-dir. İstifadəçi hansı dildə yazırsa, "
                       "sən də o dildə "
                       " səmimi girişlə başlayıb bir başa  cavab verməlisən. "
                       "Söhbət tarixçəsini yadda saxla və əvvəlki mesajlara istinad et."
)

# 2. İnterfeys elementləri
input_text = widgets.Text(placeholder='Mesajınızı yazın...', layout=widgets.Layout(width='70%'))
upload_btn = widgets.FileUpload(accept='image/*', multiple=False, description="Şəkil Seç")
button = widgets.Button(description="Göndər", button_style='primary')
clear_btn = widgets.Button(description="Yaddaşı Sil", button_style='danger')
output = widgets.Output()

def ask_gemini(b):
    global chat_history
    with output:
        if not input_text.value.strip() and not upload_btn.value:
            return
        
        clear_output()
        prompt = input_text.value.strip()
        
        try:
            # Şəkil yüklənibsə emal edilir
            image_data = None
            if upload_btn.value:
                file_info = list(upload_btn.value.values())[0]
                image_data = Image.open(io.BytesIO(file_info['content']))

            # Söhbət yaddaşını işə salırıq
            chat = model.start_chat(history=chat_history)
            
            # Şəkil və ya mətn göndərilir
            content = [prompt, image_data] if image_data else prompt
            response = chat.send_message(content)
            
            # Yeni mesajları tarixçəyə əlavə edirik (Yaddaşın əsası)
            chat_history = chat.history
            
            # Cavabı göstəririk
            display(Markdown(response.text))
            
        except Exception as e:
            display(Markdown(f"❌ *Xəta:* {e}"))
            
        input_text.value = ""
        upload_btn.value.clear()

def clear_memory(b):
    global chat_history
    chat_history = []
    with output:
        clear_output()
        display(Markdown("✨ *Yaddaş təmizləndi. Perfect AI sizi yenidən tanımaq üçün hazırdır!*"))

button.on_click(ask_gemini)
clear_btn.on_click(clear_memory)

# 3. Tətbiqi ekrana çıxarırıq
display(Markdown("# 🌟 Perfect AI"))
display(widgets.VBox([
    widgets.HBox([input_text, upload_btn, button, clear_btn]),
    output
]))
