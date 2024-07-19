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
from tkinter.scrolledtext import ScrolledText
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
faultsNo = 0 # tracks the number of faults detected in the set time period
uptimePercent = 0.0 # keeps track of the uptime percentage over a selected time period
last_accepted_start = (datetime.now() - timedelta(weeks=1)).strftime("%Y-%m-%d %H:%M:%S") #initializes the datetime to start plotting
last_accepted_end = "current time" #initializes the datetime to stop plotting

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
    global faultsNo, uptimePercent
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
    fault_times = []
    for dt, status in zip(datetimes, statuses):
        if start_datetime <= dt <= end_datetime:
            filtered_datetimes.append(dt)
            filtered_statuses.append(status)
            if status == 0:
                fault_times.append(dt.strftime("%Y-%m-%d %H:%M:%S"))

    # calculate the number of faults in this time period
    faultsNo = len(fault_times)

    # Calculate uptime percentage
    total_uptime = timedelta(0)
    total_downtime = timedelta(0)

    if len(filtered_datetimes) > 1:
        for i in range(1, len(filtered_datetimes)):
            interval = filtered_datetimes[i] - filtered_datetimes[i-1]
            if filtered_statuses[i-1] == 1:
                total_uptime += interval
            else:
                total_downtime += interval

        # Include the last interval up to the end_datetime
        if filtered_statuses[-1] == 1:
            total_uptime += end_datetime - filtered_datetimes[-1]
        else:
            total_downtime += end_datetime - filtered_datetimes[-1]

        total_time = total_uptime + total_downtime
        uptimePercent = (total_uptime / total_time) * 100 if total_time > timedelta(0) else 0.0
    else:
        uptimePercent = 100.0 if len(filtered_statuses) > 0 and filtered_statuses[0] == 1 else 0.0

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

    # Update the faults label
    faults_label.config(text="faults in period: " + str(faultsNo) + " (see datetimes below)")

    # Update the uptime label
    uptime_label.config(text=f"uptime in period: {uptimePercent:.2f}%")

    # Update the fault times in the scrolled text widget
    faults_scrolled_text.config(state=NORMAL)  # Enable editing
    faults_scrolled_text.delete(1.0, END)  # Clear current content
    for fault_time in fault_times:
        faults_scrolled_text.insert(END, fault_time + "\n")
    faults_scrolled_text.config(state=DISABLED)  # Disable editing

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
window.geometry("1000x750")

# Title across the top
title_label = Label(window, text="fSpectrum", font=('Helvetica 15 bold'))
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create a frame for the left content
left_frame = Frame(window, width=500)
left_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
left_frame.grid_propagate(False)  # Prevent the frame from resizing

# Create a frame for the right content (blank for now)
right_frame = Frame(window)
right_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Make the grid cells expand proportionally
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=2)
window.grid_rowconfigure(1, weight=1)

# ----- LEFT FRAME -----
# slider text
slider_label = Label(left_frame, text="adjust slider to set ping frequency (minutes)", font=('Helvetica 10 bold'))
slider_label.pack()

# slider (ping frequency input)
slider = Scale(left_frame, from_=1, to=120, orient=HORIZONTAL, length=400, command=get_slider)
slider.set(sliderVal)  # set default value
slider.pack()

# start button
start_button = tk.Button(left_frame, text=btnLabel, command=start_function)
start_button.pack()

# status indicator
status_canvas = Canvas(left_frame, width=300, height=16, bg="#cc3333")
statusText = status_canvas.create_text(150, 10, text="current internet status: ", fill="white", font=('Helvetica 10 bold'))
status_canvas.pack()

# ----- RIGHT FRAME -----
# subheader
statistics_label = Label(right_frame, text="statistics", font=('Helvetica 10 bold'))
statistics_label.pack()

# faults label and text
faults_label = Label(right_frame, text="faults in period: " + str(faultsNo) + " (see datetimes below)", font=('Helvetica 10'))
faults_label.pack()


# ScrolledText widget to display fault times
faults_scrolled_text = ScrolledText(right_frame, width=40, height=10, state=DISABLED)
faults_scrolled_text.pack(padx=10, pady=10, fill=X)

# uptime label and text
uptime_label = Label(right_frame, text=f"uptime in period: {uptimePercent:.2f}%", font=('Helvetica 10'))
uptime_label.pack()

# ----- DATA VISUALIZATION ----------------------------------------------------
# header
canvas2 = Canvas(left_frame, width=480, height=20)
canvas2.pack()

# Create a figure and axis for the plot
fig, ax = plt.subplots(figsize=(6, 4), dpi=100, facecolor="#f0f0f0")

# Create a Tkinter canvas and display the figure on it
fig_canvas = FigureCanvasTkAgg(fig, master=left_frame)
fig_canvas.draw()
fig_canvas.get_tk_widget().pack()

# Frame for datetime inputs
datetime_frame = Frame(left_frame)
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