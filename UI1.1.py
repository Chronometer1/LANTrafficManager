import random
from itertools import count
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))

# Set up UI window
root = tk.Tk()
root.geometry("600x400")
root.title("Graph")

# Define flag variable
capture_data = False

# Define button functions
def start_capture():
    global capture_data
    capture_data = True

def stop_capture():
    global capture_data
    capture_data = False

# Set up buttons
button_tff = ttk.Button(root, text="Train from file", command=browseFiles)
button_tfc = ttk.Button(root, text="Train from capture")
button_sc = ttk.Button(root, text="Start capture", command=start_capture)
button_ec = ttk.Button(root, text="Stop capture", command=stop_capture)
button_exit = ttk.Button(root, text="Exit", command=exit)

button_tff.pack(anchor=W)
button_tfc.pack(anchor=W)
button_sc.pack(anchor=W)
button_ec.pack(anchor=W)
button_exit.pack()

# Define blue label for the graph
label_buffer = ttk.Label(root, background="blue")
label_buffer.pack(expand=True, fill=tk.BOTH)

# Set up graph
plt.style.use('fivethirtyeight')
fig, ax = plt.subplots()
x_vals = []
y_vals = []
line, = ax.plot(x_vals, y_vals)

# Define animation function
def animate(i):
    if capture_data:
        x_vals.append(next(index))
        y_vals.append(random.randint(0,5))
        line.set_data(x_vals, y_vals)
        ax.relim()
        ax.autoscale_view()
    return line,

# Set up animation
index = count()
ani = FuncAnimation(fig, animate, frames=None, interval=1000)

# Create canvas and add to UI window
canvas = FigureCanvasTkAgg(fig, master=label_buffer)
canvas.draw()
canvas.get_tk_widget().pack(expand=True, fill=tk.BOTH)

# Start UI loop
root.mainloop()
