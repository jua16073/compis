from tkinter import *
from tkinter import filedialog


root = Tk()
root.title("hhhmmm")

def open_file():
    global archivo
    root.filename = filedialog.askopenfilename(initialdir = "/Documents/compis/", title = "Select a File", filetypes = (("all files", "*.*"), ("python", "*.py")) )
    archivo = root.filename    

menu = Menu(root)
root.config(menu = menu)
filemenu = Menu(menu)
menu.add_cascade(label = 'File', menu = filemenu)
filemenu.add_command(label = "Open File", command = open_file)
filemenu.add_separator()


frame1 = LabelFrame(root, text = "Escrito")
frame1.grid(row = 1, column = 0, pady = 10)

send_button = Button(frame1, text = "save")
send_button.grid(column = 1, row = 1)

code = Entry(frame1)
code.grid(row = 0, column = 0)

frame2 = LabelFrame(root, text = "Output")
frame2.grid(row = 1, column = 1, pady = 10)

button = Button(frame2, command = open_file)
button.grid()


# entry = Canvas(root)
# entry.grid(row = 0, column = 0, columnspan = 2)

# def myClick():
#     myLabel = Label(root, text= entry.get())
#     myLabel.grid()

# button = Button(root, text = "Enter your name", command = lambda:myClick(), bg = "blue")
# button.grid(row = 0, column = 2)

root.mainloop()
    
