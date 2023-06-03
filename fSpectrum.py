# -----------------------------------------------------------------------------
#
# fSpectrum
# a tiny downtime tool created with the help of chatGPT
# by Alex Pinson
# May 30, 2023
#
# -----------------------------------------------------------------------------

# ----- IMPORT LIBRARIES ------------------------------------------------------
import tkinter as tk # for GUI
from tkinter import *
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle

# ----- IMPORT FILES/FUNCTIONS ------------------------------------------------
from check_connection import check_internet_connection
from update_data import *

# ----- GLOBAL VARIABLES/CONSTANTS --------------------------------------------
sliderVal = 15 # this is the initial slider value
btnLabel = "running... click to stop"
stopStart = 0 #tracks how many button presses, only really relevant when 0

# ----- FUNCTION DEFINITIONS --------------------------------------------------
# gets the value of the slider input, stops the main function if it is running
def get_slider(getSlider):
    global sliderVal, runningFlag, stopStart
    sliderVal = int(getSlider)
    if runningFlag == True and stopStart > 1:
        stop_function() # stop the ping function if it's running, but only after startup (handled by > 1)
    stopStart += 1 #this needs to be here, otherwise when changing the slider before clicking the button the first time it doesn't work

# starts the uptime checker function
def start_function():
    global runningFlag, btnLabel, stopStart
    if not runningFlag:
        runningFlag = True
        btnLabel = "running... click to stop"
        start_button.config(text=btnLabel)
        run_function()
    else:
        stop_function()
    stopStart += 1

# stops the uptime checker function
def stop_function():
    global runningFlag, btnLabel
    runningFlag = False
    btnLabel = "click to start"
    start_button.config(text=btnLabel)

# when ran, this checks the status of the internet connection
def run_function():
    global runningFlag, sliderVal
    if runningFlag:
        # Do something here
        if check_internet_connection():
            print("Internet is connected!")
            log_true()
            canvas.itemconfig(statusText, text="internet status: OK as of " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            canvas.configure(bg='#7fb57f')
        else:
            print("No internet connection.")
            log_false()
            canvas.itemconfig(statusText, text="internet status: DOWN as of " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            canvas.configure(bg='#d16262')
        #plot_line_graph()
        # Schedule the function to run again after X minutes (60000 milliseconds = 1 minute)
        window.after(sliderVal*60*1000, run_function)
        
def plot_line_graph():
    data = print_entries_from_pickle()

    # Extract datetime and status from data
    datetimes = []
    statuses = []
    for entry in data:
        if isinstance(entry, dict):  # Check if entry is a dictionary
            datetimes.append(entry.get("datetime"))
            statuses.append(entry.get("connection"))

    # Convert datetimes to matplotlib-compatible format
    datetimes = [datetime.strptime(dt, "%Y-%m-%d %H:%M:%S") for dt in datetimes]

    # Create a new figure and plot the line graph
    fig = plt.figure(figsize=(6, 4), dpi=100, facecolor="#f0f0f0")
    plt.plot(datetimes, statuses)
    plt.title("uptime")
    plt.xlabel("date & time")
    plt.ylabel("status")
    plt.xticks(rotation=90)
    plt.subplots_adjust(bottom=0.4)
    
    
    # Create a Tkinter canvas and display the figure on it
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()

    # Place the canvas in the tkinter window
    canvas.get_tk_widget().pack()

runningFlag = False

# ----- TKINTER FORMATTING ----------------------------------------------------
# create window
window = tk.Tk()
window.title("fSpectrum")
window.geometry("500x700")

# header text 
canvas = Canvas(window, width= 500, height= 60)
canvas.create_text(250, 15, text="fSpectrum", fill="black", font=('Helvetica 15 bold'))
#canvas.create_text(250, 30, text="by alex pinson", fill="black", font=('Helvetica 8'))
canvas.pack()
canvas = Canvas(window, width= 500, height= 16) # spacer

# slider (ping frequency input)
canvas.create_text(250, 8, text="adjust slider to set ping frequency (minutes)", fill="black", font=('Helvetica 10 bold'))
canvas.pack()
slider = Scale(window, from_=1, to=120, orient=HORIZONTAL, length=400, command=get_slider)
slider.set(sliderVal) #set default value
slider.pack()
canvas = Canvas(window, width= 500, height= 16) # spacer
canvas.pack()

# start button
start_button = tk.Button(window, text=btnLabel, command=start_function)
start_button.pack()

# status indicator
canvas = Canvas(window, width= 300, height= 16, bg="#cc3333")
statusText = canvas.create_text(150, 10, text="internet status: ", fill="white", font=('Helvetica 10 bold'))
canvas.pack()

# ----- DATA VISUALIZATION ----------------------------------------------------
# header
canvas2 = Canvas(window, width= 500, height= 20)
canvas2.pack()

# Plot line graph
plot_line_graph()

# run once on startup to kick things off
start_function()

window.mainloop()