import tkinter as tk
from tkinter import *

from pathlib import Path

import cv2
import numpy as np

from PIL import ImageTk,Image

root = tk.Tk()

label = tk.Label(root, text="Hello, World!")
label.pack()

# Function to delete the label
def delete_label():
    label.destroy()

#Show Original Image 
    img   = Image.open('E:\Git-hab\Image_Processing_GUI\ohm1.jpg') #imread
    photo = ImageTk.PhotoImage(img) #Convert imager to Tk
    tk.Label(photo_frame, image=photo).grid(row=0,column=0)
    
# Create a button to delete the label
delete_button = tk.Button(root, text="Delete Label", command=delete_label)
delete_button.pack()

root.mainloop()