import threading
import cv2
from PIL import Image
import io
from dotenv import load_dotenv
from gtts import gTTS
import os
import tkinter as tk
from translate import Translator  # translate module
import google.generativeai as genai
import google.ai.generativelanguage as glm

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro-vision")


class ContentDescriber:
    def __init__(self, root, user_input, video_handler):
        self.root = root
        self.user_input = user_input
        self.video_handler = video_handler
        self.message_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.language_var.set("en")  # Default language (en)
        self.languages = {
            "en": "English",
            "tr": "Turkish", 
            "de": "German",  
            "ar": "Arabic",  
        }

        language_label = tk.Label(root, text="Select Language:")
        language_label.pack()

        language_menu = tk.OptionMenu(root, self.language_var, *self.languages.keys())
        language_menu.pack()

        tts_button = tk.Button(
            root, text="Text-to-Speech", width=50, command=self.text_to_speech
        )
        tts_button.pack(anchor=tk.CENTER, expand=True)

    def describe_content(self):
        current_frame = self.video_handler.get_current_frame()
        if current_frame is not None:
            pil_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format="JPEG")
            blob = glm.Blob(mime_type="image/jpeg", data=img_byte_arr.getvalue())
            user_request = self.user_input.get()
            response = model.generate_content([user_request, blob], stream=True)
            for chunk in response:
                translated_text = self.translate_text(chunk.text)
                self.root.after(0, self.update_message, translated_text)
        else:
            self.root.after(0, self.update_message, "No frame available")

    def threaded_describe_content(self):
        describe_thread = threading.Thread(target=self.describe_content)
        describe_thread.start()

    def update_message(self, new_text):
        self.message_var.set(new_text + "\n")

    def translate_text(self, text):
        selected_language = self.language_var.get()
        if selected_language in self.languages:
            target_language = selected_language
            translator = Translator(to_lang=target_language)
            translated_text = translator.translate(text)
        else:
            translated_text = text
        return translated_text

    def text_to_speech(self):
        current_text = self.message_var.get()
        selected_language = self.language_var.get()
        text_to_speech = gTTS(text=current_text, lang=selected_language, slow=False)
        text_to_speech.save("output.mp3")
        os.system(
            "start output.mp3"
        )  # Play with default media player
