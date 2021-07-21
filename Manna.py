import tkinter as tk
import cv2
import tensorflow as tf
import openpyxl as xl 

from openpyxl.chart import BarChart, Reference
from openpyxl import Workbook
from tkinter import ttk
from typing import Container
from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from tkinter import messagebox, filedialog
import numpy as np
from keras.preprocessing import image
from keras.models import load_model


classes = ['apple', 'banana', 'beetroot', 'bell pepper', 'cabbage', 'capsicum', 'carrot',
           'cauliflower', 'chilli pepper', 'corn', 'cucumber', 'eggplant', 'garlic',
           'ginger', 'grapes', 'jalepeno', 'kiwi', 'lemon', 'lettuce', 'mango', 'onion',
           'orange', 'paprika', 'pear', 'peas', 'pineapple', 'pomegranate', 'potato',
           'raddish', 'soy beans', 'spinach', 'sweetcorn', 'sweetpotato', 'tomato',
           'turnip', 'watermelon']


def show_frame(frame):
    frame.tkraise()


def createwidgets(frame):
    root.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)
    show_frame(frame1)

    frame.upload = Button(frame, text="Predict Uploaded", bg="#B5EAD7", command=lambda: FoodRec(openDirectory),
                            font=('Courier New', 15), width=16)
    frame.upload.grid(row=4, column=4)

    frame.predict = Button(frame, text="Predict Captured", bg="#B5EAD7", command=lambda: FoodRec(imgName),
                            font=('Courier New', 15), width=16)
    frame.predict.grid(row=4, column=5)

    frame.cameraLabel = Label(frame, bg="steelblue", borderwidth=3, relief="groove")
    frame.cameraLabel.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

    frame.captureBTN = Button(frame, text="CAPTURE", command=Capture, bg="#B5EAD7", font=('Courier New',15), width=20)
    frame.captureBTN.grid(row=4, column=1, padx=10, pady=10)

    frame.CAMBTN = Button(frame, text="STOP CAMERA", command=StopCAM, bg="#B5EAD7", font=('Courier New',15), width=13)
    frame.CAMBTN.grid(row=4, column=2)

    frame.previewlabel = Label(frame, fg="black", text="Let's Reduce Food Waste!", font=('Courier New',20))
    frame.previewlabel.grid(row=1, column=1, padx=10, pady=10, columnspan=2)

    frame.imageLabel = Label(frame, bg="steelblue", borderwidth=3, relief="groove")
    frame.imageLabel.grid(row=2, column=4, padx=10, pady=10, columnspan=2)

    frame.openImageEntry = Entry(frame, width=55, textvariable=imagePath)
    frame.openImageEntry.grid(row=3, column=4, padx=10, pady=10)

    frame.openImageButton = Button(frame, width=10, text="BROWSE", command=imageBrowse)
    frame.openImageButton.grid(row=3, column=5, padx=10, pady=10)

    ShowFeed()

# Defining ShowFeed() function to display webcam feed in the cameraLabel;
def ShowFeed():
    # Capturing frame1 by frame1
    ret, frame = root.cap.read()

    if ret:
        # Flipping the frame1 vertically
        frame = cv2.flip(frame, 1)

        # Displaying date and time on the feed
        cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (20,30), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))

        # Changing the frame1 color from BGR to RGB
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        # Creating an image memory from the above frame1 exporting array interface
        videoImg = Image.fromarray(cv2image)

        # Creating object of PhotoImage() class to display the frame1
        imgtk = ImageTk.PhotoImage(image = videoImg)

        # Configuring the label to display the frame1
        frame1.cameraLabel.configure(image=imgtk)

        # Keeping a reference
        frame1.cameraLabel.imgtk = imgtk

        # Calling the function after 10 milliseconds
        frame1.cameraLabel.after(10, ShowFeed)
    else:
        # Configuring the label to display the frame1
        frame1.cameraLabel.configure(image='')


def imageBrowse():
    global imageView
    global openDirectory
    # Presenting user with a pop-up for directory selection. initialdir argument is optional
    # Retrieving the user-input destination directory and storing it in destinationDirectory
    # Setting the initialdir argument is optional. SET IT TO YOUR DIRECTORY PATH
    openDirectory = filedialog.askopenfilename(initialdir="C:/Users/madar/Downloads/small-projects-main/small-projects-main")

    # Displaying the directory in the directory textbox
    imagePath.set(openDirectory)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    imageView = Image.open(openDirectory)

    # Resizing the image using Image.resize()
    imageResize = imageView.resize((640, 480), Image.ANTIALIAS)

    # Creating object of PhotoImage() class to display the frame
    imageDisplay = ImageTk.PhotoImage(imageResize)

    # Configuring the label to display the frame
    frame1.imageLabel.config(image=imageDisplay)

    # Keeping a reference
    frame1.imageLabel.photo = imageDisplay


# Defining Capture() to capture and save the image and display the image in the imageLabel
def Capture():
    global imgName
    # Storing the date in the mentioned format in the image_name variable
    image_name = datetime.now().strftime('%d-%m-%Y %H-%M-%S')

    image_path=r'C:\Users\madar\Documents\Python\SavedPics'
    # Concatenating the image_path with image_name and with .jpg extension and saving it in imgName variable
    imgName = image_path + '/' + image_name + ".jpg"

    # Capturing the frame
    ret, frame = root.cap.read()

    # Displaying date and time on the frame
    cv2.putText(frame, datetime.now().strftime('%d/%m/%Y %H:%M:%S'), (430,460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (0,255,255))
    
    # Writing the image with the captured frame. Function returns a Boolean Value which is stored in success variable
    success = cv2.imwrite(imgName, frame)

    # Opening the saved image using the open() of Image class which takes the saved image as the argument
    saved_image = Image.open(imgName)

    saved_image_flip = saved_image.transpose(Image.FLIP_LEFT_RIGHT)

    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image_flip)

    # Configuring the label to display the frame
    frame1.imageLabel.config(image=saved_image)

    # Keeping a reference
    frame1.imageLabel.photo = saved_image


def StopCAM():
    # Stopping the camera using release() method of cv2.VideoCapture()
    root.cap.release()

    # Configuring the CAMBTN to display accordingly
    frame1.CAMBTN.config(text="START CAMERA", command=StartCAM)

    # Displaying text message in the camera label
    frame1.cameraLabel.config(text="OFF CAM", font=('Courier New',70))


def StartCAM():
    # Creating object of class VideoCapture with webcam index
    root.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    # Setting width and height
    width_1, height_1 = 640, 480
    root.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width_1)
    root.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height_1)

    # Configuring the CAMBTN to display accordingly
    frame1.CAMBTN.config(text="STOP CAMERA", command=StopCAM)

    # Removing text message from the camera label
    frame1.cameraLabel.config(text="")

    # Calling the ShowFeed() Function
    ShowFeed()


def FoodRec(prev_image):
    root.cap.release()
    show_frame(frame2)

    frame2.backButton = Button(frame2, width=10, text="Back", command=lambda: createwidgets(frame1))
    frame2.backButton.grid(row=1, column=0, padx=10, pady=10)

    frame2.imageLabel = Label(frame2, bg="steelblue", borderwidth=3, relief="groove")
    frame2.imageLabel.grid(row=3, column=1, padx=10, pady=10, columnspan=2)

    Upload(prev_image)


def Upload(prev_image):
    saved_image = Image.open(prev_image)
    saved_image = saved_image.resize((640, 480), Image.ANTIALIAS)

    saved_image_flip = saved_image.transpose(Image.FLIP_LEFT_RIGHT)

    # Creating object of PhotoImage() class to display the frame
    saved_image = ImageTk.PhotoImage(saved_image_flip)
    # Configuring the label to display the frame
    frame2.imageLabel.config(image=saved_image)
    # Keeping a reference
    frame2.imageLabel.photo = saved_image

    Predict(prev_image)


def Predict(prev_image):
    global prediction

    new_model = load_model('model.h5')
    new_model.summary()
    test_image = image.load_img(
        prev_image,
        target_size=(64, 64))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)
    result = new_model.predict(test_image)
    result1 = result[0]
    for i in range(36):

        if result1[i] == 1.:
            break;
    prediction = classes[i]

    def excel():
        list.append(prediction)
        sheet.append([prediction])
        wb.save('Records.xlsx')
        print(list)
        messagebox.showinfo("SUCCESS", f'''INFORMATION RECORDED.
PRESS TRY AGAIN TO CAPTURE ANOTHER''' )

    food=f'''
    Food:{prediction}
    '''


    frame2.previewlabel = Label(frame2, fg="black", text=food, font=('Courier New',15))
    frame2.previewlabel.grid(row=3, column=6, padx=10, pady=10, columnspan=3)

    frame2.cancel = Button(frame2, text="Try Again", bg="#B5EAD7", command=lambda: createwidgets(frame1),
                            font=('Courier New', 15), width=10)
    frame2.cancel.grid(row=4, column=6)

    frame2.save = Button(frame2, text="Save", bg="#B5EAD7", command= excel,
                            font=('Courier New', 15), width=10)
    frame2.save.grid(row=4, column=7)



root = tk.Tk()
root.state('zoomed')
root.title('Ceres-Demeter-Ambrosia-Manna')

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

destPath = StringVar()
imagePath = StringVar()

global list
global sheet
list=[]

wb = xl.load_workbook('Records.xlsx')  
sheet = wb['Sheet']
    
frame1 = tk.Frame(root)
frame2 = tk.Frame(root)
frame3 = tk.Frame(root)

for frame in (frame1, frame2, frame3):
    frame.grid(row=0,column=0,sticky='nsew')


createwidgets(frame1)
root.mainloop()
