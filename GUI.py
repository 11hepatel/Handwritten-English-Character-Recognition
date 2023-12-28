#Code Inspired from this source: https://igtechteam.com/2023/06/25/handwritten-digit-recognition-part-by-part-complete-project-with-a-full-explanation/ 

import tkinter as tk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import pyscreenshot as ImageGrab
import os
import cv2
import numpy as np
from keras.models import load_model
import time

# Create the main window
window = tk.Tk()
window.title("Handwritten Character Recognition")
window.resizable(0, 0)

# Create a header label
header = tk.Button(window, width=20, height=2, bg="grey", text="Handwritten Character Recognition", font=("Helvetica", 15))
header.pack(side="top", fill="x", pady=10)

# Define a function for making predictions
def prediction():
    try:
        # Load the pre-trained model
        model = load_model("best_model.h5") 

        # Capture the handwritten input from the canvas
        img = ImageGrab.grab(bbox=(100, 150, 505, 390))
        #img = ImageGrab.grab(bbox=(235, 242, 727, 534))
        img.save("paint.png")

        # Display the captured image on the GUI
        im = cv2.imread("paint.png")
        load = Image.open("paint.png")
        load = load.resize((280, 280))
        photo = ImageTk.PhotoImage(load)
        img_label = Label(canvas3, image=photo, width=280, height=280)
        img_label.image = photo
        img_label.place(x=0, y=0)

        # Preprocess the captured image for model prediction
        im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #converts the input image to a grayscale image.
        im_gray = cv2.GaussianBlur(im_gray, (15, 15), 0) #helps in reducing image noise and smoothing out the image
        ret, im_th = cv2.threshold(im_gray, 100, 255, cv2.THRESH_BINARY)
        roi = cv2.resize(im_th, (28, 28), interpolation=cv2.INTER_AREA)
        roi = roi.reshape(28, 28, 1)
        roi = roi / 255.0
        X = np.expand_dims(roi, axis=0)

        # Make predictions using the model
        predictions = model.predict(X)
        predicted_char = chr(ord('A') + np.argmax(predictions))  # A-Z labels

        # Display the predicted character on the GUI
        prediction_label = tk.Label(canvas3, text="Prediction = " + predicted_char, font=("Times New Roman", 30), bg="light green", fg="Black")
        prediction_label.place(x=20, y=350)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

# Create Canvas1 for buttons and labels
canvas1 = Canvas(window, width=500, height=140, bg='grey')
canvas1.place(x=5, y=380)

# Create Predict button
live_prediction_button = tk.Button(canvas1, text="Predict", font=('Times new Roman', 17), bg="white", fg="Black", command=prediction)
live_prediction_button.place(x=202, y=30)

# Create Canvas2 for drawing
canvas2 = Canvas(window, width=500, height=300, bg="black")
canvas2.place(x=5, y=74)

# Function to activate paint on Canvas2
def activate_paint(e):
    global lastx, lasty
    canvas2.bind('<B1-Motion>', paint)
    lastx, lasty = e.x, e.y

# Function to draw on Canvas2
def paint(e):
    global lastx, lasty
    x, y = e.x, e.y 
    canvas2.create_line((lastx, lasty, x, y), width=15, fill="white")
    #canvas2.create_line((lastx, lasty, x, y), width=15, fill="white")
    lastx, lasty = x, y

# Bind mouse click to activate paint function
canvas2.bind('<1>', activate_paint)

# Function to clear Canvas2
def clear():
    canvas2.delete("all")

# Create Clear button
btn = tk.Button(canvas1, text="Clear", font=('Times new Roman', 17), fg="black", bg="white", command=clear)
btn.place(x=210, y=85)

# Create Canvas3 for displaying captured image and prediction
canvas3 = Canvas(window, width=280, height=447, bg="light green")
canvas3.place(x=512, y=74)

# Set the window geometry
window.geometry("800x540")

# Start the main event loop
window.mainloop()
