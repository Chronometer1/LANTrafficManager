import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

LARGE_FONT= ("Verdana", 12)


class TrafficMonitor(tk.Tk):
    
    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self,"Network traffic monitor")
        tk.Tk.wm_geometry(self,"500x300")
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
        tk.Frame.__init__(self,parent)
        button_set = ttk.Button(self, text = "Options", command = lambda:controller.show_frame(Settings)) 
        button_set.pack(anchor=NE)
        
        def browseFiles():
            filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))

        button_tfc = ttk.Button(self, text = "Train from capture", command = browseFiles)
        button_tfc.pack(pady = 5,anchor=W)

        button_sc = ttk.Button(self, text = "Start capture")
        button_sc.pack(pady = 5,anchor=W)
        

        button_exit = ttk.Button(self,text = "Exit", command = exit)
        button_exit.pack(pady = 5,anchor=W)
class Settings(ttk.Frame):
        def __init__(self, parent, controller):
            tk.Frame.__init__(self,parent)
            label = ttk.Label(self, text="Settings", font=LARGE_FONT)
            label.pack(side = "left",pady=20,padx=20)
            button_home = ttk.Button(self,text="Return",command =  lambda:controller.show_frame(HomeScreen))
            button_home.pack(side = "top")
            
            entry_depth = ttk.Entry(self)
            entry_depth.pack(side = "top")

            

        





app = TrafficMonitor()
app.mainloop()

