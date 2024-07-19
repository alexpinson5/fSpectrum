# Import necessary libraries
import tkinter as tk
from tkinter import *

# Import files & functions
from check_connection import check_internet_connection
from update_data import log_true, log_false

# Global variables & constants
sliderVal = 15 #this is the initial slider value
runState = 1 #should start active, 0 = inactive
btnLabel = "running... click to stop"

def start_button_clicked():
    global runState, btnLabel
    if runState == 1:
        runState = 0
        btnLabel = "click to begin"
        # clear all scheduled executions
        current_id = 1
        while True:
            if window.after_cancel(current_id):
                current_id += 1
            else:
                break
    else:
        runState = 1
        btnLabel = "running... click to stop"
    # Update the button label
    start_button.config(text=btnLabel)

def get_slider(getSlider):
    global sliderVal
    sliderVal = int(getSlider)
    global runState, btnLabel
    runState = 0
    btnLabel = "click to begin"
    start_button.config(text=btnLabel)

    # clear all scheduled executions
    current_id = 1
    while True:
        if window.after_cancel(current_id):
            current_id += 1
        else:
            break

def uptime_loop():
    global runState, sliderVal
    if runState == 1:
        if check_internet_connection():
            print("Internet is connected!")
            log_true()
        else:
            print("No internet connection.")
            log_false()

    window.after(1000*60*int(sliderVal), uptime_loop) 

window = tk.Tk()
window.title("fSpectrum")
window.geometry("500x300")

canvas = Canvas(window, width= 500, height= 60)
canvas.create_text(250, 15, text="fSpectrum", fill="black", font=('Helvetica 15 bold'))
canvas.create_text(250, 30, text="by alex pinson", fill="black", font=('Helvetica 8'))
canvas.pack()
canvas = Canvas(window, width= 500, height= 16)
canvas.create_text(250, 8, text="adjust slider to set ping frequency (minutes)", fill="black", font=('Helvetica 10 bold'))
canvas.pack()
slider = Scale(window, from_=1, to=120, orient=HORIZONTAL, length=400, command=get_slider)
slider.set(sliderVal) #set default value
slider.pack()
canvas = Canvas(window, width= 500, height= 16)
canvas.pack()
start_button = tk.Button(window, text=btnLabel, command=start_button_clicked)
start_button.pack()

#window.after(200, uptime_loop) #run one instance on startup

window.mainloop()