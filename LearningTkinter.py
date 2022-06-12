# learning Python Tkinter from youtube
# 11 June 2022
# https://youtu.be/NQm9VhC0vW8

from cmath import pi
from encodings import utf_8
from select import select
from tkinter import *
from tkinter import font
import tkinter.messagebox
from tkinter.colorchooser import *
from tkinter.filedialog import *
from tkinter import ttk
from turtle import right     # combo box

# First Screen
root = Tk()                     # create window
root.title("My GUI")            # set window title
# root.geometry("500x500+0+0")    # set window size

# myLabel1 = Label(root, text="Hello World!", font=20, fg="red", bg="yellow").pack()
# myLabel2 = Label(root, text="Test Programe", font=20, fg="red", bg="yellow").grid(row=0,column=1)
# myLabel3 = Label(root, text="Hi Rew", font=18, fg="white", bg="blue").place(x=200,y=50)

# Text box
# txt = StringVar()                       # string in text box
# Entry(root, textvariable=txt).pack()    # text box

# Button
# def showMSG():
#     print("func show MSG")
#     msg = txt.get()                     # get string from text box
#     Label(root, text=msg, font=20, fg="red", bg="white").pack() # display label

# def openWindow():
#     # Second Screen
#     window = Tk()
#     window.title("second screen")
#     window.geometry("500x300")

# btn1 = Button(root, text="บันทึก", fg="white", bg="red",command=showMSG).pack()
# btn2 = Button(root, text="new window", fg="white", bg="green", command=openWindow).pack()

#------------------------------------------------------------------------
# Massage Box
#------------------------------------------------------------------------
# def aboutProgram():
#     print("about Programe")
#     tkinter.messagebox.showinfo("about Program", "This Program is develop by Rew")

#------------------------------------------------------------------------
# create Menu
#------------------------------------------------------------------------
# myMenu = Menu()
# root.config(menu=myMenu)

# def showWindow():
#     window = Tk()
#     window.title("new Window")
#     window.mainloop()

# def exitProgram():
#     confirm = tkinter.messagebox.askquestion("confirm", "Are you sure Exit Program ? ")
#     if confirm == 'yes':
#         root.destroy()

# create menu item (sub menu)
# menuItem = Menu()
# menuItem.add_command(label="New Window", command=showWindow)
# menuItem.add_command(label="Open File")
# menuItem.add_command(label="Save File")
# menuItem.add_command(label="About", command=aboutProgram)
# menuItem.add_command(label="Exit", command=exitProgram)

# add main menu
# myMenu.add_cascade(label="File", menu=menuItem)
# myMenu.add_cascade(label="Edit")
# myMenu.add_cascade(label="view")

#------------------------------------------------------------------------
# Color Chooser
#------------------------------------------------------------------------
# def selectColor():
#     color = askcolor()
#     print(color[1])
#     mylabel = Label(text="Hello Color", fg="white", bg=color[1]).pack()

# btn1 = Button(text="choose color", command=selectColor).pack()

#------------------------------------------------------------------------
# Open File
#------------------------------------------------------------------------
# def selectFile():
#     # fileopen = askopenfile()      # file path with properties
#     fileopen = askopenfilename()    # file path only
#     filecontent = open(fileopen, encoding="utf8")
#     mylabel = Label(text=filecontent.read()).pack()

# btn2 = Button(text="selec file", command=selectFile).pack()

#------------------------------------------------------------------------
# Radio Button (choose only 1 choice)
#------------------------------------------------------------------------
# def  showChoice():
#     choice = language.get()
#     if choice == 1:
#         tkinter.messagebox.showinfo("notification", "you choose Python")
#     elif choice == 2:
#         tkinter.messagebox.showinfo("notification", "you choose Java")
#     elif choice == 3:
#         tkinter.messagebox.showinfo("notification", "you choose PHP")
#     else:
#         tkinter.messagebox.showinfo("notification", "you choose C#")

# language = IntVar()
# language.set(2)
# Radiobutton(text="Python", variable=language, value=1 ,command=showChoice).grid(row=0, column=0)
# Radiobutton(text="JAVA", variable=language, value=2 ,command=showChoice).grid(row=0, column=1)
# Radiobutton(text="PHP", variable=language, value=3 ,command=showChoice).grid(row=0, column=2)
# Radiobutton(text="C#", variable=language, value=4 ,command=showChoice).grid(row=0, column=3)

#------------------------------------------------------------------------
# Check Button (choose multiple choice)
#------------------------------------------------------------------------
# language1 = IntVar()
# language2 = IntVar()
# language3 = IntVar()
# language4 = IntVar()
# Checkbutton(text="Python", variable=language1).pack(anchor=W)
# Checkbutton(text="JAVA", variable=language2).pack(anchor=W)
# Checkbutton(text="PHP", variable=language3).pack(anchor=W)
# Checkbutton(text="C#", variable=language4).pack(anchor=W)

# def showChoice():
#     choice1 = language1.get()
#     choice2 = language2.get()
#     choice3 = language3.get()
#     choice4 = language4.get()
    
#     if choice1 == 1:
#         Label(text="Choose Python").pack(anchor=W)
#     if choice2 == 1:
#         Label(text="Choose Java").pack(anchor=W)
#     if choice3 == 1:
#         Label(text="Choose PHP").pack(anchor=W)
#     if choice4 == 1:
#         Label(text="Choose C#").pack(anchor=W)

# Button(text="show answer", command=showChoice).pack(anchor=W)

#------------------------------------------------------------------------
# Entry Box
#------------------------------------------------------------------------
# Label(text="Name").grid(row=0)
# Label(text="Lastname").grid(row=1)
# Label(text="Tel").grid(row=2)

# et1 = Entry()
# et1.grid(row=0, column=1)
# et1.insert(0, "Rew")
# et2 = Entry()
# et2.grid(row=1, column=1)
# et2.insert(0, "Gil")
# et3 = Entry()
# et3.grid(row=2, column=1)
# et3.insert(0, "02-xxx-xxxx")

# def clearBox():
#     et1.delete(0, END)      # delete start index, end index
#     et2.delete(0, END)
#     et3.delete(0, END)

# btn = Button(text="clear", command=clearBox).grid(row=3)

#------------------------------------------------------------------------
# Example Program Calculate Circle Area
#------------------------------------------------------------------------
# Label(text="radius", font=30).grid(row=0, sticky=W)
# radius = IntVar()
# et1 = Entry(textvariable=radius, font=30, width=30)
# et1.grid(row=0, column=1)

# Label(text="Area", font=30).grid(row=1, sticky=W)
# et2 = Entry(font=30, width=30)
# et2.grid(row=1, column=1)

# def calculate():
#     r = radius.get()
#     area = pi * r * r
#     et2.insert(0, area)

# def clear():
#     et1.delete(0, END)
#     et2.delete(0, END)

# btn1 = Button(text="Calculate", command=calculate).grid(row=2, column=1, sticky=E)
# btn2 = Button(text="Clear", command=clear).grid(row=2, column=1, sticky=W)

#------------------------------------------------------------------------
# Combo box [2:19:27]
#------------------------------------------------------------------------
# Label(text="address", font=20).grid(row=0, column=0)
# choice = StringVar(value="select your province")
# combo = ttk.Combobox(textvariable=choice)
# combo["value"] = ["Bangkok", "Chiangmai", "Nonthaburi", "Patumtani"]
# combo.grid(row=0, column=1)

# def selectCity():
#     Label(text="you select " + choice.get(), font=20).grid(row=2, column=0)

# btn = Button(text="save", command=selectCity)
# btn.grid(row=1, column=1)

#------------------------------------------------------------------------
# Currency Exchange Calculator
#------------------------------------------------------------------------
# Input
# money = IntVar()
# Label(text="Value", padx=10, font=30).grid(row=0, sticky=W)
# et1 = Entry(font=30, width=30, textvariable=money)
# et1.grid(row=0, column=1)

# choice = StringVar(value="please select currency")
# Label(text="select currency", padx=10, font=30).grid(row=1,sticky=W)
# combo = ttk.Combobox(width=30, font=30, textvariable=choice)
# combo["value"] = ["EUR", "JPY", "USD", "GBP"]
# combo.grid(row=1, column=1)

# Label(text="Result", padx=10, font=30).grid(row=2, sticky=W)
# et2 = Entry(font=30, width=30)
# et2.grid(row=2, column=1)

# def calculate():
#     amount = money.get()
#     currency = choice.get()
#     et2.delete(0, END)

#     if currency == "EUR":
#         result = str(amount * 0.026) + " EUR"
#     elif currency == "JPY":
#         result = str(amount * 3.486) + " JPY"
#     elif currency == "USD":
#         result = str(amount * 0.031) + " USD"
#     elif currency == "GBP":
#         result = str(amount * 0.023) + " GBP"
#     else:
#         result = "No Information"

#     et2.insert(0, result)

# def clear():
#     et1.delete(0, END)
#     et2.delete(0, END)

# Button(text="calculate", font=30, width=15, command=calculate).grid(row=3, column=1, sticky=W)
# Button(text="clear", font=30, width=15, command=clear).grid(row=3, column=1, sticky=E)

#------------------------------------------------------------------------
# Calculator Application
#------------------------------------------------------------------------
content = ""
txt_input = StringVar(value="0")

def btn(number):
    global content
    content = content + str(number)
    txt_input.set(content)

def equal():
    global content
    calculate = float(eval(content))
    txt_input.set(calculate)
    content = ""

def clear():
    global content
    content = ""
    txt_input.set("")
    display.insert(0, "0")

# Display 5x4
display = Entry(font=('console',30,'bold'), fg="white", bg="green", textvariable=txt_input, justify="right")
display.grid(columnspan=4)

# Input
btn7 = Button(text="7", command=lambda:btn(7), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=1, column=0)
btn8 = Button(text="8", command=lambda:btn(8), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=1, column=1)
btn9 = Button(text="9", command=lambda:btn(9), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=1, column=2)
btnClear = Button(text="C", command=clear, fg="black", bg="orange", font=('console',30,'bold'), padx=30, pady=15).grid(row=1, column=3)

btn4 = Button(text="4", command=lambda:btn(4), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=2, column=0)
btn5 = Button(text="5", command=lambda:btn(5), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=2, column=1)
btn6 = Button(text="6", command=lambda:btn(6), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=2, column=2)
btnPlus = Button(text="+", command=lambda:btn('+'), fg="black", bg="orange", font=('console',30,'bold'), padx=33, pady=15).grid(row=2, column=3)

btn1 = Button(text="1", command=lambda:btn(1), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=3, column=0)
btn2 = Button(text="2", command=lambda:btn(2), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=3, column=1)
btn3 = Button(text="3", command=lambda:btn(3), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=3, column=2)
btnMinus = Button(text="-", command=lambda:btn('-'), fg="black", bg="orange", font=('console',30,'bold'), padx=38, pady=15).grid(row=3, column=3)

btndot = Button(text=".", command=lambda:btn('.'), fg="black", font=('console',30,'bold'), padx=35, pady=15).grid(row=4, column=0)
btn0 = Button(text="0", command=lambda:btn(0), fg="black", font=('console',30,'bold'), padx=30, pady=15).grid(row=4, column=1)
btnDivide = Button(text="/", command=lambda:btn('/'), fg="black", bg="orange", font=('console',30,'bold'), padx=35, pady=15).grid(row=4, column=2)
btnMultiply = Button(text="*", command=lambda:btn('*'), fg="black", bg="orange", font=('console',30,'bold'), padx=37, pady=15).grid(row=4, column=3)

btnOpen = Button(text="(", command=lambda:btn('('), fg="black", bg="orange", font=('console',30,'bold'), padx=34, pady=15).grid(row=5, column=0)
btnClose = Button(text=")", command=lambda:btn(')'), fg="black", bg="orange", font=('console',30,'bold'), padx=34, pady=15).grid(row=5, column=1)
btnEqn = Button(text="=", command=equal, fg="black", bg="cyan", font=('console',30,'bold'), padx=91, pady=15).grid(row=5, column=2, columnspan=2)

#------------------------------------------------------------------------
root.mainloop()     # run application
