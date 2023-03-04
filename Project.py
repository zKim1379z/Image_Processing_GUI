import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path

import cv2
import numpy as np

from PIL import ImageTk,Image


global filePath
global G_rotate_img
filePath = ''

def sepia(frame):

    global filePath,sepia_img

    img_copy = cv2.imread(filePath)
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    
    #solid color
    sepia = np.ones(img_copy.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R

    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    
    sepia_img = np.array(sepia, dtype=np.uint8)
    sepia_img = cv2.cvtColor(sepia_img, cv2.COLOR_BGR2RGB)
    sepia_img = Image.fromarray(sepia_img)
    sepia_img = ImageTk.PhotoImage(sepia_img)

    tk.Label(frame, image=sepia_img).grid(row=1,column=0)

def edge_detect(frame):
    global filePath, edge
    
    img_copy = cv2.imread(filePath)

    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    edge = cv2.Canny(gray, 50, 100)
    edge = Image.fromarray(edge)
    edge = ImageTk.PhotoImage(edge)

    tk.Label(frame, image=edge).grid(row=1,column=0)

def choose_img():
    #Save state Path 
    global filePath

    # Pop up dialog for select the file with this file's parent directory
    FILE = Path(__file__).resolve()
    filePath = filedialog.askopenfilename(initialdir = FILE.parent) 

    path_label = tk.Label(first_frame,text='Path: ' + filePath).grid(row=2,column=1, pady=10)
   
def image_console():
    global G_rotate_img,filePath

    if not filePath:
        messagebox.showwarning("Error", "No image selected!")
        return
    
    # Create GUI to make Top level of that window (default = root)
    # Using only 'tk.Tk()' the program cannot find the image
    #************************************************************************************
    edit_img = tk.Toplevel()
    edit_img.title('Image Editor') 

    #Create Frame
    button_frame = tk.Frame(edit_img)
    button_frame.pack()

    photo_frame = tk.Frame(edit_img)
    photo_frame.pack()

    #Show image
    img = Image.open(filePath) #imread
    photo = ImageTk.PhotoImage(img) #Convert imager to Tk
    tk.Label(photo_frame, image=photo).grid(row=0,column=0)

    #Create Button
    rotate_cw_icon        = ImageTk.PhotoImage(Image.open('./img_res/rotate.png').resize((25,25)))
    rotate_countercw_icon = ImageTk.PhotoImage(Image.open('./img_res/counter-rotate.png').resize((25,25)))

    rotate_ccw = tk.Button(button_frame,image=rotate_countercw_icon, command=lambda: rotate_img(photo_frame, True)).grid(row=0,column=0, padx=5)
    rotate_cw  = tk.Button(button_frame,image=rotate_cw_icon,        command=lambda: rotate_img(photo_frame, False)).grid(row=0,column=1, padx=5)
    
    edge_btn  = tk.Button(button_frame, text="Edge", command=lambda: edge_detect(photo_frame)).grid(row=0, column=2, padx=5)
    sepia_btn = tk.Button(button_frame, text="Sepia",command=lambda: sepia(photo_frame)).grid(row=0, column=3, padx=5)
    
    # Set Rotage Image to Global Stage
    G_rotate_img = cv2.cvtColor(cv2.imread(filePath), cv2.COLOR_BGR2RGB)
    edit_img.mainloop()
    #************************************************************************************

def rotate_img(frame, isCounterClockwise):
  
    global roImg, G_rotate_img
    
    if isCounterClockwise == True:
        G_rotate_img = cv2.rotate(G_rotate_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        G_rotate_img = cv2.rotate(G_rotate_img, cv2.ROTATE_90_CLOCKWISE)

    roImg = Image.fromarray(G_rotate_img)
    roImg = ImageTk.PhotoImage(roImg)

    tk.Label(frame, image=roImg).grid(row=1,column=0)


#*********************************************************
#Create GUI Program
app_name = 'Image Processing'

#Page root
app_root = tk.Tk()
app_root.title(app_name)
app_root.geometry("500x200")

#Create Frame
first_frame  = tk.Frame(app_root)
first_frame.pack() #Center 

#second_frame = tk.Frame(app_root)
#second_frame.pack()
#third_frme   = tk.Frame(app_root)
#third_frme.pack()

#Create Button
take_pic_button = tk.Button(first_frame, text = 'Take a photo').grid(row=0,column=1, pady=10)
choose_button   = tk.Button(first_frame, text = 'Choose image',command = choose_img).grid(row=1,column=1, pady=10)
show_button     = tk.Button(first_frame, text = 'Show image',  command = image_console).grid(row=3,column=1, pady=10)

app_root.mainloop()
#*********************************************************

