from tkinter import *
from tkinter import filedialog


def browseFiles():
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Text files", "*.txt*"),("all files", "*.*")))

window = Tk()
window.title('Traffic Monitor Tool')
window.geometry("450x250")

button_tff = Button(window, text = "Train from file", command = browseFiles)
button_tfc = Button(window, text = "Train from capture")
button_sc = Button(window, text = "Start capture")
button_exit = Button(window, text = "Exit", command = exit)

button_tff.grid(row = 0, column = 1, pady = (10,2), padx = (4,75), sticky = W)
button_tfc.grid(row = 1, column = 1, pady = 2, padx = 4, sticky = W)
button_sc.grid(row = 2, column = 1, pady = 2, padx = 4, sticky = W)
button_exit.grid(row = 3, column = 1, pady = (100,2), padx = 4, sticky = SW)


label_buffer = Label(window, width = 35, height = 13, bg = "blue")
label_buffer.grid(column = 2, row = 0, rowspan = 4)
window.mainloop()



