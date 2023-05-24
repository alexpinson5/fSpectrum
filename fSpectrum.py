# Import necessary libraries
import tkinter as tk

# Import files & functions
from check_connection import check_internet_connection
from update_data import log_true, log_false

#def start_button_clicked():
#    print("Start button clicked!")

#window = tk.Tk()
#window.title("My App")

#start_button = tk.Button(window, text="Start", command=start_button_clicked)
#start_button.pack()

#window.mainloop()

if check_internet_connection():
    print("Internet is connected!")
    log_true()
else:
    print("No internet connection.")
    log_false()