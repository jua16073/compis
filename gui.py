from tkinter import *
from tkinter import filedialog


root = Tk()
root.title("hhhmmm")

def open_file():
    global archivo
    root.filename = filedialog.askopenfilename(initialdir = "/Documents/compis/", title = "Select a File", filetypes = (("all files", "*.*"), ("python", "*.py")) )
    archivo = root.filename    



frame1 = LabelFrame(root, text = "nani")
frame1.grid(row = 1, column = 0, pady = 10)

code = Entry(frame1)
code.grid()

frame2 = LabelFrame(root, text = "nani2")
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
    
