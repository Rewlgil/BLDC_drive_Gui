from time import time
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
        btnRead.configure(state="disable")
        btnWrite.configure(state="disable")
    else:
        rate = int(rate)
        if connectState == True:
            if port != ser.port or rate != ser.baudrate:
                disConnect()
        else:
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
    btnRead.configure(state="normal")
    btnWrite.configure(state="normal")
    connectState = True

def disConnect():
    global connectState
    print("disconnect from", ser.port, ser.baudrate)
    if connectState == True:
        ser.close()
        statusLabel.configure(text="status: disconnected", fg="#fc5203")
        cmdEntry.configure(state="disable")
        btnCon.configure(text="connect", command=makeConnect)
        btnRead.configure(state="disable")
        btnWrite.configure(state="disable")
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
        btnRead.configure(state="disable")
        btnWrite.configure(state="disable")
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
    paramOK = checkParam()
    if paramOK:
        print("Parameter OK, writing Parameter")
        cmdCode = [i for i in range(1, 23)]
        for i in [1, 5, 16, 17]:
            cmdCode.remove(i)
        print(cmdCode)
        for i in range(len(cmdCode)):
            cmdOut = "/ " + str(cmdCode[i]) + " " + str(param[i]) + "\n"
            print(cmdOut)
            ser.write(cmdOut.encode('utf_8'))
            
    else:
        print("Parameter Error please check")

def checkParam():
    global param
    
    print("checking Parameter")
    param = list()
    for i in range(len(paramVar)):
        param.append(paramVar[i].get())
    # print(param)

    paramOkay = [False for i in range(22)]
    paramOkay[0]  = param[0]  >= 5    and param[0]  <= 26
    paramOkay[1]  = param[1]  >= 2    and param[1]  <= 100
    paramOkay[2]  = param[2]  >= 0    and param[2]  <= 1
    paramOkay[3]  = param[3]  >= 8    and param[3]  <= 1023
    paramOkay[4]  = param[4]  >= 0.1  and param[4]  <= 10
    paramOkay[5]  = param[5]  >= 10   and param[5]  <= 100
    paramOkay[6]  = param[6]  >= 0.05 and param[6]  <= 6
    paramOkay[7]  = param[7]  >= 0    and param[7]  <= 1
    paramOkay[8]  = param[8]  >= 0    and param[8]  <= 1
    paramOkay[9]  = param[9]  >= 0    and param[9]  <= 16383
    paramOkay[10] = param[10] >= 0    and param[10] <= 16383
    paramOkay[11] = param[11] >= 0    and param[11] <= 16383
    paramOkay[12] = param[12] >= 0.02 and param[12] <= 50
    paramOkay[13] = param[13] >= 0.1  and param[13] <= 1000
    paramOkay[14] = param[14] >= 0.1  and param[14] <= 1000
    paramOkay[15] = param[15] >= 0.1  and param[15] <= 1000
    paramOkay[16] = param[16] >= 0.1  and param[16] <= 1000
    paramOkay[17] = param[17] >= 0.1  and param[17] <= 1000
    paramOkay[18] = param[18] >= 0    and param[18] <= 1000
    paramOkay[19] = param[19] >= 0    and param[19] <= 1000
    paramOkay[20] = param[20] >= 0    and param[20] <= 1000
    paramOkay[21] = param[21] >= 0    and param[21] <= 1000

    allParamOk = True
    errorParam = list()
    for i in range(22):
        allParamOk &= paramOkay[i]
        if paramOkay[i] == False:
            errorParam.append(i)
    if errorParam != []:
        print("Error Parameter No.", errorParam)
    # print("Parameter Okay =", allParamOk)
    
    return allParamOk

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
            textBox.see("end")

    root.after(100, mainLoop)

def main():
    global root
    global portCombo, btnCon, statusLabel
    global portChoice, rateChoice
    global textBox, cmdEntry, cmd
    global connectState, port
    global paramVar
    global btnRead, btnWrite

    root = Tk()
    root.title("BLDC driver config")
    root.geometry("+600+0")

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
    btnRefresh.grid(row=0, column=2)

    btnCon = Button(text="Connect", command=makeConnect, state="disable")
    btnCon.grid(row=1, column=2)

    statusLabel = Label(text="status: disconnected", fg="#fc5203")
    statusLabel.grid(row=2, column=2)

    # row 3 ~ 12 parameter list
    paramVar = list()
    paramEntry = list()
    
    for i in range(22):
        paramVar.append(DoubleVar(value=1))
    
    for i in range(22):
        paramEntry.append(Entry(textvariable=paramVar[i]))
        paramEntry[i].grid(row=i+3, column=1)

    Label(text="Voltage Source").grid(row=3, column=0)
    Label(text="[5-26 : -1]").grid(row=3, column=2)
    
    Label(text="Motor PolePair").grid(row=4, column=0)
    Label(text="[2-100 : -1]").grid(row=4, column=2)
    
    Label(text="Motor Direction").grid(row=5, column=0)
    Label(text="[0-1 : -1]").grid(row=5, column=2)

    Label(text="PWM Resolution").grid(row=6, column=0)
    Label(text="[8-1023]").grid(row=6, column=2)
    
    Label(text="Time Test").grid(row=7, column=0)
    Label(text="[0.1-10 : -1]").grid(row=7, column=2)

    Label(text="Voltage Test").grid(row=8, column=0)
    Label(text="[10-100 : -1]").grid(row=8, column=2)
    
    Label(text="Velocity Test").grid(row=9, column=0)
    Label(text="[0.05-6 : -1]").grid(row=9, column=2)

    Label(text="Open-Loop Drive").grid(row=10, column=0)
    Label(text="[0 : 1]").grid(row=10, column=2)
    
    Label(text="Encoder Direction").grid(row=11, column=0)
    Label(text="[0 : 1 : -1]").grid(row=11, column=2)

    Label(text="Rotor Offset CW").grid(row=12, column=0)
    Label(text="[0-16383 : -1]").grid(row=12, column=2)

    Label(text="Rotor Offset CCW").grid(row=13, column=0)
    Label(text="[0-16383 : -1]").grid(row=13, column=2)

    Label(text="Shaft Offset").grid(row=14, column=0)
    Label(text="[0-16383 : -1]").grid(row=14, column=2)
    
    Label(text="Gear Ratio").grid(row=15, column=0)
    Label(text="[0.02-50 : -1]").grid(row=15, column=2)

    Label(text="Limit Velocity").grid(row=16, column=0)
    Label(text="[0.1-1000]").grid(row=16, column=2)
    
    Label(text="Max Velocity").grid(row=17, column=0)
    Label(text="[0.1-1000]").grid(row=17, column=2)

    Label(text="Min Velocity").grid(row=18, column=0)
    Label(text="[0.1-1000]").grid(row=18, column=2)
    
    Label(text="Acceleration").grid(row=19, column=0)
    Label(text="[0.1-1000]").grid(row=19, column=2)

    Label(text="Deceleration").grid(row=20, column=0)
    Label(text="[0.1-1000]").grid(row=20, column=2)
    
    Label(text="Position P-Gain").grid(row=21, column=0)
    Label(text="[0-1000]").grid(row=21, column=2)

    Label(text="Position I-Gain").grid(row=22, column=0)
    Label(text="[0-1000]").grid(row=22, column=2)

    Label(text="Velocity P-Gain").grid(row=23, column=0)
    Label(text="[0-1000]").grid(row=23, column=2)

    Label(text="Velocity I-Gain").grid(row=24, column=0)
    Label(text="[0-1000]").grid(row=24, column=2)

    # row 25 read write parameter button
    btnRead = Button(text="Read parameter", command=readParam, state="disable")
    btnRead.grid(row=25, column=0)

    btnWrite = Button(text="Write parameter", command=writeParam, state="disable")
    btnWrite.grid(row=25, column=1)

    # row 26 ~ 28 serial monitor
    Label(text="Serial monitor").grid(row=26, column=0)
    textBox = Text(width=40, heigh=5, state="disable")
    textBox.grid(row=27, column=0, columnspan=3)

    cmd = StringVar()
    cmdEntry = Entry(textvariable=cmd, width=53, state="disable")
    cmdEntry.bind('<Return>', readCMD)
    cmdEntry.grid(row=28, column=0, columnspan=3)

    root.after(100, mainLoop)
    root.mainloop()

if __name__ == '__main__':
    main()