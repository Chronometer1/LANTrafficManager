import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
import random
plt.cla()

LARGE_FONT= ("Verdana", 12)


class TrafficMonitor(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Network traffic monitor")
        tk.Tk.wm_geometry(self,"850x600")
        tk.Tk.configure(self)
        container=ttk.Frame(self,height=100,width=100)
        container.pack(side="top",fill="both",expand=True)
        container.grid_rowconfigure(100, weight=1)
        container.grid_columnconfigure(100, weight=1)
        self.frames = {}
        
        for F in (HomeScreen,Settings):
            
            frame = F(container, self)
            
            self.frames[F] = frame
            
            frame.grid(row=100,column=100,sticky="nsew")
        
        self.show_frame(HomeScreen)
        
    def show_frame(self,cont):
            frame = self.frames[cont]
            frame.tkraise()


class HomeScreen(ttk.Frame):
     def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent,bg="seashell3")
        
        
        def browseFiles():
            filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))
        capture_data = False

# Define button functions
        def start_capture():
            global capture_data
            capture_data = True

        def stop_capture():
            global capture_data
            capture_data = False
        
        #Create toolbar for buttons 
        toolbar = Frame(self,bg="darkorange")

        label_Title = tk.Label(toolbar,bg="seashell3",text = "NUWC Network Traffic Monitor",font=LARGE_FONT)
        label_Title.pack(pady=10,side=TOP)

        button_set = tk.Button(toolbar,bg="seashell3", text = "Options", command = lambda:controller.show_frame(Settings)) 
        button_set.pack(padx = 10,pady = 10,side = LEFT,anchor=NE)

        button_tfc = tk.Button(toolbar,bg="seashell3", text = "Train from capture", command = browseFiles)
        button_tfc.pack(padx = 10,pady = 10,side = LEFT,anchor=NW)

        button_sc = tk.Button(toolbar,bg="seashell3", text = "Start capture", command=start_capture)
        button_sc.pack(padx = 10,pady = 10,side = LEFT,anchor=NW)

        button_sc = tk.Button(toolbar,bg="seashell3", text = "Stop capture", command=stop_capture)
        button_sc.pack(padx = 10,pady = 10,side = LEFT,anchor=NW)
        
        button_exit = tk.Button(toolbar,bg="seashell3",text = "Exit", command = exit)
        button_exit.pack(padx = 10,pady = 10,side = LEFT,anchor=NW)

        

        toolbar.pack(side=TOP,fill=X)
        #Graph stuff 
        label_buffer = ttk.Label(self,background="seashell3")
        label_buffer.pack(expand=True, fill=tk.BOTH)
        plt.style.use('fivethirtyeight')
        self.fig, ax = plt.subplots()
        x_vals = []
        y_vals = []
        self.line, = ax.plot(x_vals, y_vals)

        # Define animation function
        def animate(i):
            if capture_data:
                x_vals.append(next(index))
                y_vals.append(random.randint(0,5))
                self.line.set_data(x_vals, y_vals)
                ax.relim()
                ax.autoscale_view()
            return self.line,

        # Set up animation
        index = count()
        self.ani = FuncAnimation(self.fig, animate, frames=None, interval=1000)

        # Create canvas and add to UI window
        canvas = FigureCanvasTkAgg(self.fig, master=label_buffer)
        canvas.draw()
        canvas.get_tk_widget().pack()
        


class Settings(ttk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self,parent,bg="seashell3")
            label = ttk.Label(self, text="Settings", font=LARGE_FONT)
            label.pack(side = "left",pady=20,padx=20)
            button_home = ttk.Button(self,text="Return",command = lambda:controller.show_frame(HomeScreen))
            button_home.pack(side = "top")
            
            entry_depth = ttk.Entry(self)
            entry_depth.pack(side = "top")

            

        





app = TrafficMonitor()
app.mainloop()
