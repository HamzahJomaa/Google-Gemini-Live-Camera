import tkinter as tk
from video_stream import VideoStreamHandler
from content_description import ContentDescriber

root = tk.Tk()
root.title("Webcam Stream")

root.tk_setPalette(background="#85001B", foreground="#FFFFFF")
root.option_add("*TButton*highlightBackground", "#2C2C2C")
root.option_add("*TButton*highlightColor", "#2C2C2C")
root.option_add("*TButton*foreground", "#FFFFFF")

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()
canvas.config(bg="#2C2C2C", highlightthickness=0)

user_input = tk.Entry(root, width=50)
user_input.pack()

video_handler = VideoStreamHandler(root, canvas)
content_describer = ContentDescriber(root, user_input, video_handler)

root.mainloop()
