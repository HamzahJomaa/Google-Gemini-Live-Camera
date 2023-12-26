import tkinter as tk
from video_stream import VideoStreamHandler
from content_description import ContentDescriber

# Main GUI setup and button handlers
root = tk.Tk()
root.title("Webcam Stream")

user_input = tk.Entry(root, width=50)
user_input.pack()

canvas = tk.Canvas(root, width=640, height=480)
canvas.pack()

video_handler = VideoStreamHandler(root, canvas)
content_describer = ContentDescriber(root, user_input, video_handler)

button = tk.Button(root, text="Stop", width=50, command=video_handler.stop_video)
button.pack(anchor=tk.CENTER, expand=True)

describe_button = tk.Button(root, text="Describe the frame", width=50, command=content_describer.threaded_describe_content)
describe_button.pack(anchor=tk.CENTER, expand=True)

message_label = tk.Label(root, textvariable=content_describer.message_var, wraplength=500)
message_label.pack()

video_handler.start_stream()

root.mainloop()
