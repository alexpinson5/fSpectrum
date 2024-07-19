# -----------------------------------------------------------------------------
#
# fSpectrum
# a tiny downtime tool created with the help of chatGPT
# by Alex Pinson
# May 30, 2023
#
# -----------------------------------------------------------------------------

# ----- IMPORT PACKAGES ------------------------------------------------------
from package_checker import check_and_install_packages  # import package checker file

packages = [
    "tkinter",
    "datetime",
    "matplotlib",
    "pickle"
]
check_and_install_packages(packages)

import tkinter as tk  # for GUI
from tkinter import *
from tkinter import ttk
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pickle

# ----- IMPORT FILES/FUNCTIONS ------------------------------------------------
from check_connection import check_internet_connection
from update_data import *

# ----- GLOBAL VARIABLES/CONSTANTS --------------------------------------------
sliderVal = 15  # this is the initial slider value
btnLabel = "running... click to stop"
stopStart = 0  # tracks how many button presses, only really relevant when 0

# ----- FUNCTION DEFINITIONS --------------------------------------------------
# gets the value of the slider input, stops the main function if it is running
def get_slider(getSlider):
    global sliderVal, runningFlag, stopStart
    sliderVal = int(getSlider)
    if runningFlag == True and stopStart > 1:
        stop_function()  # stop the ping function if it's running, but only after startup (handled by > 1)
    stopStart += 1  # this needs to be here, otherwise when changing the slider before clicking the button the first time it doesn't work

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
            status_canvas.itemconfig(statusText, text="internet status: OK as of " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            status_canvas.configure(bg='#7fb57f')
        else:
            print("No internet connection.")
            log_false()
            status_canvas.itemconfig(statusText, text="internet status: DOWN as of " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            status_canvas.configure(bg='#d16262')

        plot_line_graph()
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

    # Filter data based on the selected date range
    start_datetime = datetime.strptime(start_datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
    end_datetime = datetime.strptime(end_datetime_entry.get(), "%Y-%m-%d %H:%M:%S") if end_datetime_entry.get() != 'current time' else datetime.now()
    
    filtered_datetimes = []
    filtered_statuses = []
    for dt, status in zip(datetimes, statuses):
        if start_datetime <= dt <= end_datetime:
            filtered_datetimes.append(dt)
            filtered_statuses.append(status)

    ax.clear()  # clear the existing plot

    # Plot the new data
    ax.plot(filtered_datetimes, filtered_statuses)
    ax.set_title("uptime")
    ax.set_xlabel("date & time")
    ax.set_ylabel("status")
    plt.setp(ax.get_xticklabels(), rotation=90)

    # Format the x-axis to show the year, month, date, hour, and minute
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
    plt.setp(ax.get_xticklabels(), rotation=90)
    
    # Adjust layout to prevent the dates from being cut off
    fig.tight_layout(rect=[0, 0.1, 1, 1])

    # Update the Tkinter canvas with the new figure
    fig_canvas.draw()

def print_entries_from_pickle():
    try:
        with open("data.pickle", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []
    
# Function to set datetime fields based on the selected option
def set_datetime_fields(*args):
    now = datetime.now()
    if time_range_var.get() == "Last Hour":
        start_time = now - timedelta(hours=1)
    elif time_range_var.get() == "Last 12 Hours":
        start_time = now - timedelta(hours=12)
    elif time_range_var.get() == "Last Day":
        start_time = now - timedelta(days=1)
    elif time_range_var.get() == "Last Week":
        start_time = now - timedelta(weeks=1)
    elif time_range_var.get() == "Last Month":
        start_time = now - timedelta(days=30)
    elif time_range_var.get() == "Last Quarter":
        start_time = now - timedelta(days=90)
    elif time_range_var.get() == "Last Year":
        start_time = now - timedelta(days=365)
    elif time_range_var.get() == "All Time":
        start_time = datetime.min
    else:
        return

    start_datetime_entry.delete(0, END)
    start_datetime_entry.insert(0, start_time.strftime("%Y-%m-%d %H:%M:%S"))
    end_datetime_entry.delete(0, END)
    end_datetime_entry.insert(0, "current time")
    
# Initialize the last accepted datetime values
last_accepted_start = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M:%S")
last_accepted_end = "current time"

def validate_and_plot():
    global last_accepted_start, last_accepted_end
    try:
        # Validate start datetime
        start_datetime = datetime.strptime(start_datetime_entry.get(), "%Y-%m-%d %H:%M:%S")
        last_accepted_start = start_datetime_entry.get()
    except ValueError:
        tk.messagebox.showerror("Invalid Input", "Start datetime format is incorrect. Reverting to last accepted value.")
        start_datetime_entry.delete(0, END)
        start_datetime_entry.insert(0, last_accepted_start)
        return

    try:
        # Validate end datetime
        end_datetime_input = end_datetime_entry.get()
        if end_datetime_input.lower() != 'current time':
            end_datetime = datetime.strptime(end_datetime_input, "%Y-%m-%d %H:%M:%S")
            last_accepted_end = end_datetime_entry.get()
        else:
            last_accepted_end = "current time"
    except ValueError:
        tk.messagebox.showerror("Invalid Input", "End datetime format is incorrect. Reverting to last accepted value.")
        end_datetime_entry.delete(0, END)
        end_datetime_entry.insert(0, last_accepted_end)
        return

    # If validation passes, update the plot
    plot_line_graph()

runningFlag = False

# ----- TKINTER FORMATTING ----------------------------------------------------
# create window
window = tk.Tk()
window.title("fSpectrum")
window.geometry("500x750")

# header text
header_canvas = Canvas(window, width=500, height=60)
header_canvas.create_text(250, 15, text="fSpectrum", fill="black", font=('Helvetica 15 bold'))
header_canvas.pack()

# slider text
slider_label = Label(window, text="adjust slider to set ping frequency (minutes)", font=('Helvetica 10 bold'))
slider_label.pack()

# slider (ping frequency input)
slider = Scale(window, from_=1, to=120, orient=HORIZONTAL, length=400, command=get_slider)
slider.set(sliderVal)  # set default value
slider.pack()

# start button
start_button = tk.Button(window, text=btnLabel, command=start_function)
start_button.pack()

# status indicator
status_canvas = Canvas(window, width=300, height=16, bg="#cc3333")
statusText = status_canvas.create_text(150, 10, text="current internet status: ", fill="white", font=('Helvetica 10 bold'))
status_canvas.pack()

# ----- DATA VISUALIZATION ----------------------------------------------------
# header
canvas2 = Canvas(window, width=500, height=20)
canvas2.pack()

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor="#f0f0f0")

# Create a Tkinter canvas and display the figure on it
fig_canvas = FigureCanvasTkAgg(fig, master=window)
fig_canvas.draw()
fig_canvas.get_tk_widget().pack()

# Frame for datetime inputs
datetime_frame = Frame(window)
datetime_frame.pack()

# Drop-down menu for time range options
time_range_var = StringVar(window)
time_range_options = ["Last Hour", "Last 12 Hours", "Last Day", "Last Week", "Last Month", "Last Quarter", "Last Year", "All Time"]
time_range_var.set("Last Week")  # Default value
time_range_label = Label(datetime_frame, text="Quick Presets:", font=('Helvetica 10 bold'))
time_range_label.grid(row=0, column=0, sticky=E)
time_range_menu = ttk.OptionMenu(datetime_frame, time_range_var, time_range_var.get(), *time_range_options, command=set_datetime_fields)
time_range_menu.grid(row=0, column=1, padx=10, pady=5, sticky=W)

# Start datetime selector
start_datetime_label = Label(datetime_frame, text="Start Datetime (YYYY-MM-DD HH:MM:SS):", font=('Helvetica 10 bold'))
start_datetime_label.grid(row=1, column=0, sticky=E)
start_datetime_entry = ttk.Entry(datetime_frame)
start_datetime_entry.grid(row=1, column=1, padx=10, pady=5)
start_datetime_entry.insert(0, last_accepted_start)

# End datetime selector
end_datetime_label = Label(datetime_frame, text="End Datetime (YYYY-MM-DD HH:MM:SS) or 'current time':", font=('Helvetica 10 bold'))
end_datetime_label.grid(row=2, column=0, sticky=E)
end_datetime_entry = ttk.Entry(datetime_frame)
end_datetime_entry.grid(row=2, column=1, padx=10, pady=5)
end_datetime_entry.insert(0, last_accepted_end)

# Update plot button
update_button = tk.Button(datetime_frame, text="Update Plot", command=validate_and_plot)
update_button.grid(row=3, column=1, padx=10, pady=10, sticky=E)

# Plot line graph
plot_line_graph()

# run once on startup to kick things off
start_function()

window.mainloop()