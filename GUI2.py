from tkinter import *
from tkinter import ttk
import serial
import serial.tools.list_ports

def serialList():
    return [p[0] for p in list(serial.tools.list_ports.comports())]

def connectionSetted(event):
    global port, rate
    port = portChoice.get()
    rate = rateChoice.get()
    print(port, ",", rate)

    if port == "No availabel port" or port == "Select port" or rate == "Select baud rate":
        btnCon.configure(text="connect", state="disable")
    else:
        rate = int(rate)
        if connectState == True:
            if port != ser.port or rate != ser.baudrate:
                disConnect()
        btnCon.configure(text="connect", command=makeConnect, state="normal")

def makeConnect():
    global ser, connectState
    print("connectting to", port, rate)
    if connectState == True:
        ser.close()
    ser = serial.Serial(port, rate, timeout=0.1)
    if ser.is_open == False:
        ser.open()

    statusLabel.configure(text="status: Connected", fg="#269900")
    cmdEntry.configure(state="normal")
    btnCon.configure(text="disconnect", command=disConnect)
    connectState = True

def disConnect():
    global connectState
    print("disconnect from", ser.port, ser.baudrate)
    if connectState == True:
        ser.close()
        statusLabel.configure(text="status: disconnected", fg="#fc5203")
        cmdEntry.configure(state="disable")
        btnCon.configure(text="connect", command=makeConnect)
    connectState = False

def refresh():
    global port
    print("refresh")
    availablePort = serialList()

    if connectState == True:
        if ser.port not in availablePort:
            disConnect()
    
    portCombo.configure(values=availablePort)
    if availablePort == []:
        print("no available port")
        portChoice.set("No availabel port")
        portCombo.configure(state="disable")
        btnCon.configure(state="disable")
    elif len(availablePort) == 1:
        print("found", availablePort)
        portCombo.configure(state="readonly")
        portCombo.current(0)
        port = availablePort[0]
        connectionSetted("call")
    else:
        print("found", availablePort)
        portCombo.configure(state="readonly")

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
    print(">", cmdStr)
    ser.write(cmdStr.encode('utf_8'))
    textBox.configure(state="normal")
    textBox.insert(END, '>' + cmdStr + '\n')
    textBox.configure(state="disable")
    cmdEntry.delete(0, END)
    textBox.see("end")

def mainLoop():
    if connectState == True:
        # ser.flush()
        if ser.inWaiting() > 0:
            answer=""
            while ser.inWaiting() > 0:
                answer += str(ser.readline()).replace("\\r","").replace("\\n","").replace("'","").replace("b","")
            print(answer)
            textBox.configure(state="normal")
            textBox.insert(END, answer + '\n')
            textBox.configure(state="disable")

    root.after(100, mainLoop)

def main():
    global root
    global portCombo, btnCon, statusLabel
    global portChoice, rateChoice
    global textBox, cmdEntry, cmd
    global connectState, port

    root = Tk()
    root.title("BLDC driver config")

    connectState = False

    # row 0 port setting
    Label(root, text="COM Port").grid(row=0, column=0)
    availablePort = serialList()
    portChoice = StringVar(value="Select port")
    portCombo = ttk.Combobox(textvariable=portChoice, values=availablePort)

    if availablePort == []:
        print("no available port")
        portChoice.set("No availabel port")
        portCombo.configure(state="disable")
    elif len(availablePort) == 1:
        print("found", availablePort)
        portCombo.configure(state="readonly")
        portCombo.current(0)
        port = availablePort[0]
    else:
        print("found", availablePort)
        portCombo.configure(state="readonly")

    portCombo.bind("<<ComboboxSelected>>", connectionSetted)
    portCombo.grid(row=0, column=1)

    # row 1 baud rate setting
    Label(root, text="baud rate").grid(row=1, column=0)
    rateChoice = StringVar(value="Select baud rate")
    rateCombo = ttk.Combobox(textvariable=rateChoice, state="readonly")
    rateCombo["value"] = [9600, 115200, 1000000, 2000000]
    rateCombo.bind("<<ComboboxSelected>>", connectionSetted)
    rateCombo.grid(row=1, column=1)

    # row 2 button
    btnRefresh = Button(text="Refresh", command=refresh)
    btnRefresh.grid(row=2, column=0)

    btnCon = Button(text="Connect", command=makeConnect, state="disable")
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

    # row 14 ~ 16 serial monitor
    Label(text="Serial monitor").grid(row=14, column=0)
    textBox = Text(width=40, heigh=5, state="disable")
    textBox.grid(row=15, column=0, columnspan=3)

    cmd = StringVar()
    cmdEntry = Entry(textvariable=cmd, width=53, state="disable")
    cmdEntry.bind('<Return>', readCMD)
    cmdEntry.grid(row=16, column=0, columnspan=3)

    root.after(100, mainLoop)
    root.mainloop()

if __name__ == '__main__':
    main()