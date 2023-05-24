import tkinter as tk

def start_button_clicked():
    print("Start button clicked!")

window = tk.Tk()
window.title("My App")

start_button = tk.Button(window, text="Start", command=start_button_clicked)
start_button.pack()

window.mainloop()