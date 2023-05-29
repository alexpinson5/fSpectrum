import tkinter as tk

def start_function():
    global running_flag
    if not running_flag:
        running_flag = True
        run_function()

def stop_function():
    global running_flag
    running_flag = False

def run_function():
    global running_flag
    if running_flag:
        # Do something here
        print("Function running...")
        # Schedule the function to run again after X minutes (60000 milliseconds = 1 minute)
        root.after(1000, run_function)

running_flag = False

# Create the tkinter window
root = tk.Tk()

# Create the Start button
start_button = tk.Button(root, text="Start", command=start_function)
start_button.pack()

# Create the Stop button
stop_button = tk.Button(root, text="Stop", command=stop_function)
stop_button.pack()

# Start the tkinter event loop
root.mainloop()