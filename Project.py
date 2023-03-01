import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

import cv2
from PIL import ImageTk,Image

global filePath
filePath = ''

def choose_img():
    FILE = Path(__file__).resolve()
    global filePath
    filePath = filedialog.askopenfilename(initialdir=FILE.parent) # Pop up dialog for select the file with this file's parent directory
    
    path_label = tk.Label(second_frame,text='Path: ' +filePath)
    path_label.grid(row=3,column=1, pady=10)

def show_btn():
    if not filePath:
        messagebox.showwarning("Error", "No image selected!")
        return
    # Create GUI to make Top level of that window (default = root)
    # Using only 'tk.Tk()' the program cannot find the image
    edit_img = tk.Toplevel() 

    first_frame = tk.Frame(edit_img)
    first_frame.pack()
    take_pic_button = tk.Button(first_frame,text='Take a photo')
    take_pic_button.grid(row=0,column=1, pady=10)

    img = Image.open(filePath)
    photo = ImageTk.PhotoImage(img)
    tk.Label(edit_img, image=photo).pack()

    edit_img.title('Image Editor')
    edit_img.mainloop()


app_name = 'Image Processing'


app_root = tk.Tk()
first_frame = tk.Frame(app_root)
first_frame.pack()
second_frame = tk.Frame(app_root)
second_frame.pack()
third_frme = tk.Frame(app_root)
third_frme.pack()

take_pic_button = tk.Button(first_frame,text='Take a photo')
take_pic_button.grid(row=0,column=1, pady=10)
choose_button = tk.Button(second_frame,text='Choose image',command=choose_img)
choose_button.grid(row=2,column=1, pady=10)
show_button = tk.Button(third_frme,text='Show image',command=show_btn)
show_button.grid(row=4,column=1, pady=10)

app_root.geometry("500x200")
app_root.title(app_name)
app_root.mainloop()


