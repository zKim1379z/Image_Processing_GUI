# import tkinter as tk
# from tkinter import filedialog
# from tkinter import messagebox
# from pathlib import Path

# import cv2
# from PIL import ImageTk,Image


# ws = tk.Tk()
# ws.title('PythonGuides')


# img = ImageTk.PhotoImage(file="C:/Users/pasaw/Desktop/Code Project/Python/Digital image/Project/index.jpg")
# tk.Label(
#     ws,
#     image=img
# ).pack()

# ws.mainloop()

from tkinter import *
from PIL import Image, ImageTk

# Create a Tkinter window
window = Tk()

# Open the image using Pillow
image = Image.open("C:/Users/pasaw/Desktop/Code Project/Python/Digital image/Project/index.jpg")

# Create a Tkinter PhotoImage from the Pillow Image
photo = ImageTk.PhotoImage(image)

# Create a label in the window and add the PhotoImage to it
label = Label(window, image=photo)
label.pack()

# Run the Tkinter event loop
window.mainloop()