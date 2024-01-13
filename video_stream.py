import cv2
from PIL import Image, ImageTk
import tkinter as tk


class VideoStreamHandler:
    def __init__(self, root, canvas):
        self.root = root
        self.canvas = canvas
        self.cap = None
        self.photo = None
        self.current_frame = None
        self.after_id = None

    def start_stream(self, camera_index):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(int(camera_index))
        self.update_video_stream()
        self.after_id = self.root.after(10, self.video_stream)

    def start_stream(self, camera_index):
        if self.cap is not None:
            self.cap.release()
        self.cap = cv2.VideoCapture(int(camera_index))
        thread = threading.Thread(target=self.video_stream)
        thread.start()

    def video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)

            if self.photo:
                self.photo.paste(img)
            else:
                self.photo = ImageTk.PhotoImage(image=img)
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            self.after_id = self.root.after(10, self.video_stream)

    def update_video_stream(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            self.photo = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

    def stop_video(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.root.after_cancel(self.after_id)

    def get_current_frame(self):
        return self.current_frame
