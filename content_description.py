import threading
import cv2
from PIL import Image
import io
from dotenv import load_dotenv
import os
import tkinter as tk
import google.generativeai as genai
import google.ai.generativelanguage as glm

load_dotenv()
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
model = genai.GenerativeModel('gemini-pro-vision')

class ContentDescriber:
    def __init__(self, root, user_input, video_handler):
        self.root = root
        self.user_input = user_input
        self.video_handler = video_handler
        self.message_var = tk.StringVar()

    def describe_content(self):
        current_frame = self.video_handler.get_current_frame()
        if current_frame is not None:
            pil_image = Image.fromarray(cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB))
            img_byte_arr = io.BytesIO()
            pil_image.save(img_byte_arr, format='JPEG')
            blob = glm.Blob(
                mime_type='image/jpeg',
                data=img_byte_arr.getvalue()
            )
            user_request = self.user_input.get()
            response = model.generate_content([user_request, blob], stream=True)
            for chunk in response:
                self.root.after(0, self.update_message, chunk.text)
        else:
            self.root.after(0, self.update_message, "No frame available")

    def threaded_describe_content(self):
        describe_thread = threading.Thread(target=self.describe_content)
        describe_thread.start()

    def update_message(self, new_text):
        current_text = self.message_var.get()
        updated_text = current_text + new_text + "\n"
        self.message_var.set(updated_text)
