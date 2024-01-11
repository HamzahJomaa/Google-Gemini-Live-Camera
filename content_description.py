import threading
import cv2
from PIL import Image, ImageTk
import io
from dotenv import load_dotenv
from gtts import gTTS
import os
import tkinter as tk
from translate import Translator
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
        self.language_var.set("en")
        self.languages = {
            "en": "English",
            "tr": "Turkish",
            "de": "German",
            "ar": "Arabic",
        }

        self.camera_var = tk.StringVar()
        self.camera_var.set("0")

        frame_main = tk.Frame(root)
        frame_main.pack()

        frame_language_camera = tk.Frame(frame_main)
        frame_language_camera.pack(side=tk.TOP)

        camera_label = tk.Label(frame_language_camera, text="Select Camera:")
        camera_label.pack(side=tk.LEFT, padx=5, pady=5)

        camera_menu = tk.OptionMenu(
            frame_language_camera, self.camera_var, *self.get_available_cameras()
        )
        camera_menu.pack(side=tk.LEFT, padx=5, pady=5)

        language_label = tk.Label(frame_language_camera, text="Select Language:")
        language_label.pack(side=tk.LEFT, padx=5, pady=5)

        language_menu = tk.OptionMenu(
            frame_language_camera, self.language_var, *self.languages.keys()
        )
        language_menu.pack(side=tk.LEFT, padx=5, pady=5)

        self.message_label = tk.Label(
            frame_main, textvariable=self.message_var, wraplength=500, anchor=tk.E
        )
        self.message_label.pack(side=tk.BOTTOM)

        frame_buttons = tk.Frame(frame_main)
        frame_buttons.pack(side=tk.TOP)

        frame_buttons_top = tk.Frame(frame_buttons)
        frame_buttons_top.pack(side=tk.TOP)

        frame_buttons_bottom = tk.Frame(frame_buttons)
        frame_buttons_bottom.pack(side=tk.TOP)

        button_stop = tk.Button(
            frame_buttons_top, text="Stop", width=50, command=video_handler.stop_video
        )
        button_stop.pack(side=tk.LEFT, padx=5, pady=5)

        button_describe = tk.Button(
            frame_buttons_top,
            text="Describe the frame",
            width=50,
            command=lambda: self.threaded_describe_content(),
        )
        button_describe.pack(side=tk.LEFT, padx=5, pady=5)

        button_tts = tk.Button(
            frame_buttons_top,
            text="Text-to-Speech",
            width=50,
            command=self.text_to_speech,
        )
        button_tts.pack(side=tk.LEFT, padx=5, pady=5)

        button_camera = tk.Button(
            frame_buttons_bottom,
            text="Select Camera",
            width=50,
            command=lambda: video_handler.start_stream(self.camera_var.get()),
        )
        button_camera.pack(side=tk.TOP, padx=5, pady=5)

    def get_available_cameras(self):
        available_cameras = []
        for i in range(10):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                available_cameras.append(str(i))
                cap.release()
        return available_cameras

    def describe_content(self):
        self.message_var.set("")

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
        current_text = self.message_var.get()
        if current_text:
            updated_text = current_text + "\n" + new_text
        else:
            updated_text = new_text
        self.message_var.set(updated_text)

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
        os.system("start output.mp3")
