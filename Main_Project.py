import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import *
from pathlib import Path

import cv2
import os
import numpy as np

from PIL import ImageTk,Image


global filePath, G_rotation_angle, G_filter_state, photoImage, state_img

filePath = ''

def choose_img():
    #Save state Path 
    global filePath

    # Pop up dialog for select the file with this file's parent directory
    FILE = Path(__file__).resolve()
    filePath = filedialog.askopenfilename(initialdir = FILE.parent) 

    tk.Label(first_frame,text='Path: ' + filePath).grid(row=2,column=1, pady=10)
   
def image_console():
    global G_rotation_angle, filePath , G_filter_state

    if not filePath:
        messagebox.showwarning("Error", "No image selected!")
        return
    
    # Create GUI to make Top level of that window (default = root)
    # Using only 'tk.Tk()' the program cannot find the image
    #************************************************************************************
    edit_img = tk.Toplevel()
    edit_img.title('Image Editor') 
    edit_img.geometry("1200x800")
    
    #Create Frame
    button_frame = tk.Frame(edit_img)
    button_frame.pack()

    photo_frame  = tk.Frame(edit_img)
    photo_frame.pack(expand=True, pady=25)
 
    # store array image (for openCV)
    array_img = cv2.imread(filePath) # got array of image

    # Show Original Image
    OriginImg = cv2.cvtColor(array_img, cv2.COLOR_BGR2RGB)
    showImg(OriginImg, photo_frame)

    # Create Button
    rotate_cw_icon        = ImageTk.PhotoImage(Image.open('./img_res/rotate.png').resize((25,25)))
    rotate_countercw_icon = ImageTk.PhotoImage(Image.open('./img_res/counter-rotate.png').resize((25,25)))

    tk.Button(button_frame,image=rotate_countercw_icon, command=lambda: rotate_img(array_img, photo_frame, True)) .grid(row=0,column=0, padx=5)
    tk.Button(button_frame,image=rotate_cw_icon,        command=lambda: rotate_img(array_img, photo_frame, False)).grid(row=0,column=1, padx=5)
    
    tk.Button(button_frame, text="Origin", command=lambda: originImg(OriginImg, photo_frame))  .grid(row=0, column=2, padx=5)
    tk.Button(button_frame, text="Edge", command=lambda: edge(array_img, photo_frame))  .grid(row=0, column=3, padx=5)
    tk.Button(button_frame, text="Sepia",command=lambda: sepia(array_img, photo_frame)) .grid(row=0, column=4, padx=5)
    tk.Button(button_frame, text="Ghost",command=lambda: invert(array_img, photo_frame)).grid(row=0, column=5, padx=5)
    tk.Button(button_frame, text="RedOnly",command=lambda: red_filter(array_img, photo_frame)).grid(row=0, column=6, padx=5)

    # Save image button 
    tk.Button(button_frame, text="Save", command=lambda: saveImg()).grid(row=1, column=3)

    # Set Rotage Image to Global State
    G_rotation_angle = 0
    # Set filter state to Global State
    G_filter_state = 'normal'

    edit_img.mainloop()
    #************************************************************************************

def showImg(img, frame):
    global photoImage, state_img

    resize_img = resizeImg(img)
    image = Image.fromarray(resize_img)
    photoImage = ImageTk.PhotoImage(image) 

    # set Stage image for save method
    state_img = img

    #Displays images as specified position.
    tk.Label(frame, image=photoImage).grid(row=0,column=0)

def resizeImg(img):

    # default scale_percent
    scale_percent = 100

    # resize condition *(sharp[0] = height, sharp[1] = weight)*
    if (img.shape[1] >= 2500 or img.shape[0] >= 2500):
        scale_percent = 25
    elif (img.shape[1] >= 1300 or img.shape[0] >= 900):
        scale_percent = 50

    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
  
    # resize image
    return cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

def rotate_img(img, frame, isCounterClockwise):
  
    global G_rotation_angle
    
    # Check filter state
    rotate_img = checkFilterState(img)

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
    
    rgbImg = cv2.cvtColor(rotate_img, cv2.COLOR_BGR2RGB)

    # Show Image
    showImg(rgbImg, frame)

def checkFilterState(img):
    global G_filter_state

    if (G_filter_state == 'normal'):
        result = img
    elif (G_filter_state == 'red_filter'):
        result = red_filter_method(img)
    elif (G_filter_state == 'invert'):
        result = invert_method(img)
    elif (G_filter_state == 'sepia'):
        result = sepia_method(img)
    elif (G_filter_state == 'edge'):
        result = edge_method(img)

    return result

#Fucntion about All Filter
#*******************************************************************

def originImg(img, frame):
    global G_filter_state

    # resize img
    resize_img = resizeImg(img)
    # cal rotation
    roImg = calRotation(resize_img)
    # show Image
    showImg(roImg, frame)
    # set global filter State
    G_filter_state = 'normal'

def red_filter(img, frame):
    global G_filter_state

    # filter image
    added_img =  red_filter_method(img)

    # call Rotation 
    roImg = calRotation(added_img)

    bgrImg = cv2.cvtColor(roImg, cv2.COLOR_BGR2RGB)
    showImg(bgrImg, frame)

    # Set filter state to Global State
    G_filter_state = 'red_filter'

def red_filter_method(img):

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

    return added_img

def invert(img, frame):
    global G_filter_state

    # filter image
    invert_img = invert_method(img)
    
    # call Rotation 
    roImg = calRotation(invert_img)

    showImg(roImg, frame)

    # Set filter state to Global State
    G_filter_state = 'invert'

def invert_method(img):
    img_gray   = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    invert_img = cv2.bitwise_not(img_gray)

    return invert_img

def sepia(img, frame):
    global G_filter_state

    # filter image
    sepia_img = sepia_method(img)

    # call Rotation 
    roImg = calRotation(sepia_img)

    roImg = cv2.cvtColor(roImg, cv2.COLOR_BGR2RGB)
    showImg(roImg, frame)

    # Set filter state to Global State
    G_filter_state = 'sepia'

def sepia_method(img):
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

    return sepia_img

def edge(img, frame):
    global edge_img, G_filter_state

    edge_img = edge_method(img)

    # call Rotation 
    roImg = calRotation(edge_img)

    showImg(roImg, frame)

    # Set filter state to Global State
    G_filter_state = 'edge'

def edge_method(img):

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edge_img = cv2.Canny(gray, 50, 100)

    return edge_img

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

# Save Image method
def saveImg():

    global state_img, filePath, G_filter_state
    
    FILE = Path(__file__).resolve()

    # Get string file path
    img_name = filePath.split('/')
    img_name = img_name[-1].split('.')

    # Create New save Img name
    img_name = img_name[0]

    if (G_filter_state != 'normal'):
        img_name += f'_{G_filter_state}'

    # Save image to spacific path (need to cvt bgr to rgb)
    state_img_rgb = cv2.cvtColor(state_img, cv2.COLOR_BGR2RGB)
    cv2.imwrite(f'{FILE.parent}\save_image\{img_name}.jpg', state_img_rgb) 

    messagebox.showinfo("Success", "Save Image.")

#Main 
#*********************************************************

#Create GUI Program
app_name = 'Image Filter Program'

#Page root
app_root = tk.Tk()
app_root.title(app_name)
app_root.geometry("500x250")

#Create Frame
first_frame  = tk.Frame(app_root)
first_frame.pack() #Center 

#Create Button
# take_pic_button = tk.Button(first_frame, text = 'Take a photo').grid(row=0,column=1, pady=10)

tk.Label(first_frame, text = 'Image Filter Program', font=("Arial", 25)).grid(row=1,column=1, pady=15)

choose_button   = tk.Button(first_frame, text = 'Choose image',command = choose_img)   .grid(row=3,column=1, pady=10)
show_button     = tk.Button(first_frame, text = 'Show image',  command = image_console).grid(row=5,column=1, pady=10)

app_root.mainloop()
#*********************************************************

