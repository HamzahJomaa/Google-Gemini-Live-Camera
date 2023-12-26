import cv2
import threading
from PIL import Image, ImageTk
import tkinter as tk


class VideoStreamHandler:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.cap = cv2.VideoCapture(0)
        self.photo = None
        self.current_frame = None

    def video_stream(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = frame
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(cv2image)
                self.photo = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
                self.root.update()

    def start_stream(self):
        thread = threading.Thread(target=self.video_stream)
        thread.start()

    def stop_video(self):
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()

    def get_current_frame(self):
        return self.current_frame
