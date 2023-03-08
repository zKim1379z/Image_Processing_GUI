import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from pathlib import Path

import cv2
import numpy as np

from PIL import ImageTk,Image


global filePath, G_rotation_angle, G_filter_state

filePath = ''

def choose_img():
    #Save state Path 
    global filePath

    # Pop up dialog for select the file with this file's parent directory
    FILE = Path(__file__).resolve()
    filePath = filedialog.askopenfilename(initialdir = FILE.parent) 

    path_label = tk.Label(first_frame,text='Path: ' + filePath).grid(row=2,column=1, pady=10)
   
def image_console():
    global G_rotation_angle, filePath , img_onshow, G_filter_state

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

    photo_frame  = tk.Frame(edit_img)
    photo_frame.pack()

    #Show Original Image 
    img   = Image.open(filePath) #imread
    cvt_photo = ImageTk.PhotoImage(img) #Convert img to Tk
    img_onshow = tk.Label(photo_frame, image=cvt_photo).grid(row=0,column=0)
    
    #Create Button
    rotate_cw_icon        = ImageTk.PhotoImage(Image.open('./img_res/rotate.png').resize((25,25)))
    rotate_countercw_icon = ImageTk.PhotoImage(Image.open('./img_res/counter-rotate.png').resize((25,25)))

    rotate_ccw = tk.Button(button_frame,image=rotate_countercw_icon, command=lambda: rotate_img(photo_frame, True)) .grid(row=0,column=0, padx=5)
    rotate_cw  = tk.Button(button_frame,image=rotate_cw_icon,        command=lambda: rotate_img(photo_frame, False)).grid(row=0,column=1, padx=5)
    
    edge_btn   = tk.Button(button_frame, text="Edge", command=lambda: edge(photo_frame))  .grid(row=0, column=2, padx=5)
    sepia_btn  = tk.Button(button_frame, text="Sepia",command=lambda: sepia(photo_frame)) .grid(row=0, column=3, padx=5)
    invert_btn = tk.Button(button_frame, text="Ghost",command=lambda: invert(photo_frame)).grid(row=0, column=4, padx=5)
    red_only_btn = tk.Button(button_frame, text="RedOnly",command=lambda: red_filter(photo_frame)).grid(row=0, column=5, padx=5)

    #btn = tk.Button(button_frame, text="Reset",command=lambda: ).grid(row=0, column=6, padx=5)


    # Set Rotage Image to Global State
    G_rotation_angle = 0
    # Set filter state to Global State
    G_filter_state = 'normal'

    edit_img.mainloop()
    #************************************************************************************

def rotate_img(frame, isCounterClockwise):
  
    global G_rotation_angle, filePath
    
    #read the image
    rotate_img = cv2.imread(filePath)

    if isCounterClockwise == True:
        if G_rotation_angle == 0:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            G_rotation_angle = 270

        elif G_rotation_angle == 270:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_180)
            G_rotation_angle = 180

        elif G_rotation_angle == 180:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_90_CLOCKWISE)
            G_rotation_angle = 90

        elif G_rotation_angle == 90:
            G_rotation_angle = 0

    else:
        if G_rotation_angle == 0:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_90_CLOCKWISE)
            G_rotation_angle = 90

        elif G_rotation_angle == 90:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_180)
            G_rotation_angle = 180

        elif G_rotation_angle == 180:
            rotate_img = cv2.rotate(rotate_img, cv2.ROTATE_90_COUNTERCLOCKWISE)
            G_rotation_angle = 270

        elif G_rotation_angle == 270:
            G_rotation_angle = 0
    
    cv2.imshow('', rotate_img)

    rgb = cv2.cvtColor(rotate_img, cv2.COLOR_BGR2RGB)
    roImg = Image.fromarray(rgb)
    roImg = ImageTk.PhotoImage(roImg)

    tk.Label(frame, image=roImg).grid(row=0,column=0)

#Fucntion about All Filter
#*******************************************************************
def red_filter(frame, checkRotation = True):
    global filePath, red_filter_img, G_filter_state

    #read the image
    img = cv2.imread(filePath)
    #convert the BGR image to HSV colour space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    #obtain the grayscale image of the original image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #set the bounds for the red hue
    lower_red = np.array([160,100,50])
    upper_red = np.array([180,255,255])

    #create a mask using the bounds set
    mask = cv2.inRange(hsv, lower_red, upper_red)
    #create an inverse of the mask
    mask_inv = cv2.bitwise_not(mask)
    #Filter only the red colour from the original image using the mask(foreground)
    res = cv2.bitwise_and(img, img, mask=mask)
    #Filter the regions containing colours other than red from the grayscale image(background)
    background = cv2.bitwise_and(gray, gray, mask = mask_inv)
    #convert the one channelled grayscale background to a three channelled image
    background = np.stack((background,) * 3, axis=-1)
    #add the foreground and the background
    added_img = cv2.add(res, background)

    # call Rotation 
    if (checkRotation == True):
        roImg = calRotation(added_img)

    cv2.imshow('', roImg)

    bgr = cv2.cvtColor(roImg, cv2.COLOR_BGR2RGB)
    red_filter_img = Image.fromarray(bgr)
    red_filter_img = ImageTk.PhotoImage(red_filter_img) 

    #Displays images as specified position.
    tk.Label(frame, image=red_filter_img).grid(row=0,column=0)

    # Set filter state to Global State
    G_filter_state = 'red_filter'

def invert(frame, checkRotation = True):
    global filePath, invert_img, G_filter_state

    img = cv2.imread(filePath)
    img_gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert_img = cv2.bitwise_not(img_gray)
    
    # call Rotation 
    if (checkRotation == True):
        roImg = calRotation(invert_img)

    cv2.imshow('', roImg)

    invert_img = Image.fromarray(roImg)
    invert_img = ImageTk.PhotoImage(invert_img)

    #Displays images as specified position.
    tk.Label(frame, image=invert_img).grid(row=0,column=0)

    # Set filter state to Global State
    G_filter_state = 'invert'

def sepia(frame, checkRotation = True):
    global filePath, sepia_img, G_filter_state

    img  = cv2.imread(filePath)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    normalized_gray = np.array(gray, np.float32)/255
    
    #solid color
    sepia = np.ones(img.shape)
    sepia[:,:,0] *= 153 #B
    sepia[:,:,1] *= 204 #G
    sepia[:,:,2] *= 255 #R

    #hadamard
    sepia[:,:,0] *= normalized_gray #B
    sepia[:,:,1] *= normalized_gray #G
    sepia[:,:,2] *= normalized_gray #R
    
    sepia_img = np.array(sepia, dtype=np.uint8)
    sepia_img = cv2.cvtColor(sepia_img, cv2.COLOR_BGR2RGB)

    # call Rotation 
    if (checkRotation == True):
        roImg = calRotation(sepia_img)

    cv2.imshow('', roImg)

    sepia_img = Image.fromarray(roImg)
    sepia_img = ImageTk.PhotoImage(sepia_img)

    tk.Label(frame, image=sepia_img).grid(row=0,column=0)

    # Set filter state to Global State
    G_filter_state = 'sepia'

def edge(frame, checkRotation = True):
    global filePath, edge_img, G_filter_state
    
    img = cv2.imread(filePath)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge_img = cv2.Canny(gray, 50, 100)

    # call Rotation 
    if (checkRotation == True):
        roImg = calRotation(edge_img)

    cv2.imshow('', roImg)

    edge_img = Image.fromarray(roImg)
    edge_img = ImageTk.PhotoImage(edge_img)

    #Displays images as specified position.
    tk.Label(frame, image=edge_img).grid(row=0,column=0)

    # Set filter state to Global State
    G_filter_state = 'edge'

def calRotation(image):
    global G_rotation_angle

    if G_rotation_angle == 0:
        img = image

    elif G_rotation_angle == 90:
        img = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    elif G_rotation_angle == 180:
        img = cv2.rotate(image, cv2.ROTATE_180)

    elif G_rotation_angle == 270:
        img = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

    return img

# def calFilterState(image):
#     global G_filter_state

#     if (G_filter_state == 'red_filter'):
#         red_filter(image)


#*******************************************************************

#Main 
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
choose_button   = tk.Button(first_frame, text = 'Choose image',command = choose_img)   .grid(row=1,column=1, pady=10)
show_button     = tk.Button(first_frame, text = 'Show image',  command = image_console).grid(row=3,column=1, pady=10)

app_root.mainloop()
#*********************************************************

