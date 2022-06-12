from os import stat
from tkinter import *

def readCMD(event):
    cmdStr = cmd.get() 
    # print(cmdStr)
    textBox.configure(state="normal")
    textBox.insert(END, '>' + cmdStr + '\n')
    textBox.configure(state="disable")
    cmdEntry.delete(0, END)
    textBox.see("end")

root = Tk()
root.geometry("500x500+800+100")

textBox = Text(width=50, heigh=5, state="disable")
textBox.grid(row=0, column=0, padx=40)

cmd = StringVar()
cmdEntry = Entry(textvariable=cmd, width=65)
cmdEntry.bind('<Return>', readCMD)
cmdEntry.grid(row=1, column=0, padx=40)

root.mainloop()