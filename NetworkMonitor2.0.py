import random
from itertools import count
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Set up UI window
root = tk.Tk()
root.geometry("600x450")
root.title("Traffic Monitor")

# Set up notebook
notebook = ttk.Notebook(root)
notebook.pack(fill='both', expand=True)

# Define flag variable
capture_data = False

# Define button functions
def start_capture():
    global capture_data
    capture_data = True

def stop_capture():
    global capture_data
    capture_data = False

def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))
    
# Home Tab
Home = ttk.Frame(notebook)
notebook.add(Home, text='Home')

button_ex = ttk.Button(Home, text="Exit",command= exit)
button_ex.pack(anchor=E)

button_tfc = ttk.Button(Home, text="Train from capture")
button_tfc.pack(anchor=W)

button_sc = ttk.Button(Home, text="Start capture", command=start_capture)
button_sc.pack(anchor=W)

button_ec = ttk.Button(Home, text="Stop capture", command=stop_capture)
button_ec.pack(anchor=W)

button_tff = ttk.Button(Home, text="Train from file", command=browseFiles)
button_tff.pack(anchor=W)

# Define blue label for the graph
label_buffer = ttk.Label(Home, background="blue")
label_buffer.pack(expand=True, fill=tk.BOTH)

# settings Tab
Settings = ttk.Frame(notebook)
notebook.add(Settings, text='Settings')

maxDep = tk.StringVar()
numEst = tk.StringVar()
ranSta = tk.StringVar()
MaxFea = tk.StringVar()
MinSam = tk.StringVar()
MaxLea = tk.StringVar()
AbnThr = tk.StringVar()

max_depth = tk.Entry(Settings,textvariable=maxDep)
max_depth.pack(fill='both',pady=10)
maxDep.set("Enter value for max depth")

Num_Est = tk.Entry(Settings,textvariable=numEst)
Num_Est.pack(fill='both',pady=10)
numEst.set("Enter Value for Number of Estimates")

Random_St = tk.Entry(Settings,textvariable=ranSta)
Random_St.pack(fill='both',pady=10)
ranSta.set("Enter Random State")

Max_Fea = tk.Entry(Settings,textvariable=MaxFea)
Max_Fea.pack(fill='both',pady=10)
MaxFea.set("Enter the max Features")

Min_Sam = tk.Entry(Settings,textvariable=MinSam)
Min_Sam.pack(fill='both',pady=10)
MinSam.set("Enter Minimum Samples")

Max_Lea = tk.Entry(Settings,textvariable=MaxLea)
Max_Lea.pack(fill='both',pady=10)
MaxLea.set("Enter Max Layers")

Abn_Thr = tk.Entry(Settings,textvariable=AbnThr)
Abn_Thr.pack(fill='both',pady=10)
AbnThr.set("Enter Abnormality Threashold")

Apply = tk.Button(Settings,text="Apply")
Apply.pack()







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
