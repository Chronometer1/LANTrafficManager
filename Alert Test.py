from tkinter import * 
from tkinter import messagebox
  
root = Tk()
root.geometry("10x10")
  
w = Label(root, text ='Alert test', font = "50") 
w.pack()
  
x = messagebox.askquestion("Abnormality detected", "Abnormal activity detected from: [example connection] \nIt has been detected [number] times. \nMark as normal?")

print (x)

  
root.mainloop() 
