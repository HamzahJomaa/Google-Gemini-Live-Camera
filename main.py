import tkinter as tk
from video_stream import VideoStreamHandler
from content_description import ContentDescriber

root = tk.Tk()
root.title("Webcam Stream")

user_input = tk.Entry(root, width=50)
user_input.pack()

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

video_handler = VideoStreamHandler(root, canvas)
content_describer = ContentDescriber(root, user_input, video_handler)

root.mainloop()
