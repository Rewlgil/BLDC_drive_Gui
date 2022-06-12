from tkinter import *
from tkinter import ttk

from GUI import refresh

def makeConnect():
    print("connectted")
    statusLabel.configure(text="status: Connected", fg="#269900")
    btnCon.configure(text="disconnect", command=disConnect, bg="#fc5203")

def disConnect():
    print("disconnectted")
    statusLabel.configure(text="status: disconnected", fg="#fc5203")
    btnCon.configure(text="connect", command=makeConnect, bg="#269900")

def refresh():
    print("refresh")

def readParam():
    print("read Parameter")

def writeParam():
    checkParam()
    print("write Parameter")

def checkParam():
    print("check Parameter")

def readCMD(event):
    global cmdStr

    cmdStr = cmd.get()
    # print(cmdStr)
    textBox.configure(state="normal")
    textBox.insert(END, '>' + cmdStr + '\n')
    textBox.configure(state="disable")
    cmdEntry.delete(0, END)
    textBox.see("end")

def mainLoop():
    pass

def main():
    global portCombo, rateCombo, btnRefresh, btnCon, statusLabel, textBox, cmdEntry, cmd

    root = Tk()
    root.title("BLDC driver config")

    # row 0 port setting
    Label(root, text="COM Port").grid(row=0, column=0)
    availablePort = ["COM1", "COM2"]
    portChoice = StringVar(value="No availabel port")
    portCombo = ttk.Combobox(textvariable=portChoice, values=availablePort)
    portCombo.grid(row=0, column=1)

    # row 1 baud rate setting
    Label(root, text="baud rate").grid(row=1, column=0)
    rateChoice = StringVar(value="Select baud rate")
    rateCombo = ttk.Combobox(textvariable=rateChoice, state="readonly")
    rateCombo["value"] = [2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200]
    rateCombo.grid(row=1, column=1)

    # row 2 button
    btnRefresh = Button(text="Refresh", command=refresh)
    btnRefresh.grid(row=2, column=0)

    btnCon = Button(text="Connect", command=makeConnect)
    btnCon.grid(row=2, column=1)

    statusLabel = Label(text="status: disconnected", fg="#fc5203")
    statusLabel.grid(row=2, column=2)

    # row 3 ~ 12 parameter list
    param1 = IntVar()
    param2 = IntVar()
    param3 = IntVar()
    param4 = IntVar()
    param5 = IntVar()
    param6 = IntVar()
    param7 = IntVar()
    param8 = IntVar()
    param9 = IntVar()
    param10 = IntVar()

    Label(text="Parameter 1").grid(row=3, column=0)
    Label(text="[unit 1]").grid(row=3, column=2)
    param1Entry = Entry(textvariable=param1).grid(row=3, column=1)

    Label(text="Parameter 2").grid(row=4, column=0)
    Label(text="[unit 2]").grid(row=4, column=2)
    param2Entry = Entry(textvariable=param2).grid(row=4, column=1)
    
    Label(text="Parameter 3").grid(row=5, column=0)
    Label(text="[unit 3]").grid(row=5, column=2)
    param3Entry = Entry(textvariable=param3).grid(row=5, column=1)

    Label(text="Parameter 4").grid(row=6, column=0)
    Label(text="[unit 4]").grid(row=6, column=2)
    param4Entry = Entry(textvariable=param4).grid(row=6, column=1)
    
    Label(text="Parameter 5").grid(row=7, column=0)
    Label(text="[unit 5]").grid(row=7, column=2)
    param5Entry = Entry(textvariable=param5).grid(row=7, column=1)

    Label(text="Parameter 6").grid(row=8, column=0)
    Label(text="[unit 6]").grid(row=8, column=2)
    param6Entry = Entry(textvariable=param6).grid(row=8, column=1)
    
    Label(text="Parameter 7").grid(row=9, column=0)
    Label(text="[unit 7]").grid(row=9, column=2)
    param7Entry = Entry(textvariable=param7).grid(row=9, column=1)

    Label(text="Parameter 8").grid(row=10, column=0)
    Label(text="[unit 8]").grid(row=10, column=2)
    param8Entry = Entry(textvariable=param8).grid(row=10, column=1)
    
    Label(text="Parameter 9").grid(row=11, column=0)
    Label(text="[unit 9]").grid(row=11, column=2)
    param9Entry = Entry(textvariable=param9).grid(row=11, column=1)

    Label(text="Parameter 10").grid(row=12, column=0)
    Label(text="[unit 10]").grid(row=12, column=2)
    param10Entry = Entry(textvariable=param10).grid(row=12, column=1)

    # row 13 read write parameter button
    btnRead = Button(text="Read parameter", command=readParam)
    btnRead.grid(row=13, column=0)

    btnWrite = Button(text="Write parameter", command=writeParam)
    btnWrite.grid(row=13, column=1)

    # row 14 ~ 16 debug terminal
    Label(text="Debugger").grid(row=14, column=0)
    textBox = Text(width=40, heigh=5, state="disable")
    textBox.grid(row=15, column=0, columnspan=3)

    cmd = StringVar()
    cmdEntry = Entry(textvariable=cmd, width=53)
    cmdEntry.bind('<Return>', readCMD)
    cmdEntry.grid(row=16, column=0, columnspan=3)

    root.mainloop()

if __name__ == '__main__':
    main()