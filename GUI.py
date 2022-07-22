from tkinter import *
from tkinter import ttk
import serial
import serial.tools.list_ports
import time

def serialList():
    return [p[0] for p in list(serial.tools.list_ports.comports())]

def connectionSetted(event):
    global port, rate
    port = portChoice.get()
    rate = rateChoice.get()
    print(port, ",", rate)

    if port == "No availabel port" or port == "Select port" or rate == "Select baud rate":
        disConnect()
        btnCon.configure(text="connect", state="disable")
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
    put2TextBox("connectting to " + str(port) + " " + str(rate) + '\n')
    if connectState == True:
        ser.close()
    ser = serial.Serial(port, rate, timeout=0.1)
    if ser.is_open == False:
        ser.open()
    serConnectted()

def serConnectted():
    global connectState

    if connectState == False:
        connectState = True
        statusLabel.configure(text="status: Connected", fg="#269900")
        cmdEntry.configure(state="normal")
        btnCon.configure(text="disconnect", command=disConnect)
        btnRead.configure(state="normal")
        btnWrite.configure(state="normal")
        btnRebt.configure(state="normal")
        btnMotor.configure(text="Enable", state="normal")
        btnCtrMod.configure(state="normal")
        btnOPdiv1.configure(state="normal")
        btnOPdiv2.configure(state="normal")
        btnCLdiv1.configure(state="normal")
        btnCLdiv2.configure(state="normal")
        btnGetAng.configure(state="normal")
        btnGetAngH.configure(state="normal")

def disConnect():
    global connectState
    
    if connectState == True:
        print("disconnect from", ser.port, ser.baudrate)
        put2TextBox("disconnect from" + str(port) + str(rate) + '\n')
        ser.close()
        connectState = False
    
    MotorEnState = False

    statusLabel.configure(text="status: disconnected", fg="#fc5203")
    cmdEntry.configure(state="disable")
    btnCon.configure(text="connect", command=makeConnect)
    btnRead.configure(state="disable")
    btnWrite.configure(state="disable")
    btnRebt.configure(state="disable")
    btnMotor.configure(text="Enable", state="disable")
    btnCtrMod.configure(state="disable")
    btnOPdiv1.configure(state="disable")
    btnOPdiv2.configure(state="disable")
    btnCLdiv1.configure(state="disable")
    btnCLdiv2.configure(state="disable")
    btnGetAng.configure(state="disable")
    btnGetAngH.configure(state="disable")


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
        disConnect()
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
    param_read = list()
    print("read Parameter")
    cmdOut = "/ 31 1\n"
    ser.write(cmdOut.encode('utf_8'))
    
    start_waiting = time.time()
    while ser.inWaiting() == 0:
        time.sleep(0.1)
        if time.time() - start_waiting > 0.5:
            print("Time out waiting no response")
            put2TextBox("Time out waiting no response\n")
            btnRead.configure(state="normal")
            return

    if ser.inWaiting() > 0:
        answer = ""
        answer_str = ""
        
        while ser.inWaiting() > 0:
            answer = ser.readline()
            answer_str += answer.decode()
        answer_str = answer_str.strip('\n').strip('\r')
        print(answer_str)
        param_read = answer_str.split('\t')
        
        if param_read[0] == '/':
            param_read.remove('/')
            print(param_read)
            for i in range(len(param_read)):
                paramVar[i].set(float(param_read[i]))

def writeParam():
    global param
    
    param = list()
    for i in range(len(paramVar)):
        param.append(paramVar[i].get())
    
    # paramOK = checkParam()
    
    # if paramOK:
    if True:
        # print("Parameter OK, writing Parameter")
        # put2TextBox("Parameter OK, writing Parameter\n")
        cmdCode = [i for i in range(1, len(param)+1)]
        # print(cmdCode)
        for i in range(len(cmdCode)):
            if i in range(21, 25):
                cmdOut = "/ " + str(cmdCode[i]) + " " + format(param[i], '.7f') + "\n"
            else:
                cmdOut = "/ " + str(cmdCode[i]) + " " + str(param[i]) + "\n"
            print(cmdOut, end='')
            put2TextBox(">> " + cmdOut)
            ser.write(cmdOut.encode('utf_8'))

        cmdOut = "/ 30 1\n"
        ser.write(cmdOut.encode('utf_8'))
        print(cmdOut, end='')
        put2TextBox(">> " + cmdOut)
        
    else:
        print("Parameter Error please check")
        put2TextBox("Parameter Error please check\n")

# def checkParam():
#     global param
    
#     print("checking Parameter")
#     param = list()
#     for i in range(len(paramVar)):
#         param.append(paramVar[i].get())
#     # print(param)

#     paramOkay = [False for i in range(25)]
#     paramOkay[0]  = param[0]  >= 1         and param[0]  <= 254
#     paramOkay[1]  = param[1]  >= 0         and param[1]  <= 2
#     paramOkay[2]  = param[2]  >= 5         and param[2]  <= 26
#     paramOkay[3]  = param[3]  >= 0.1       and param[3]  <= 8.5
#     paramOkay[4]  = param[4]  >= 30        and param[4]  <= 80
#     paramOkay[5]  = param[5]  >= 1         and param[5]  <= 24
#     paramOkay[6]  = param[6]  >= 0         and param[6]  <= 1
#     paramOkay[7]  = param[7]  >= 0         and param[7]  <= 16383
#     paramOkay[8]  = param[8]  >= 0         and param[8]  <= 16383
#     paramOkay[9]  = param[9]  >= 0         and param[9]  <= 16383
#     paramOkay[10] = param[10] >= 0.001     and param[10] <= 1000
#     paramOkay[11] = param[11] >= 16        and param[11] <= 1024
#     paramOkay[12] = param[12] >= 0         and param[12] <= 1
#     paramOkay[13] = param[13] >= 0.5       and param[13] <= 15
#     paramOkay[14] = param[14] >= 10        and param[14] <= 100
#     paramOkay[15] = param[15] >= 0.00174   and param[15] <= 2.617
#     paramOkay[16] = param[16] >= 0.0174    and param[16] <= 1884.95
#     paramOkay[17] = param[17] >= 0.0174    and param[17] <= 1884.95
#     paramOkay[18] = param[18] >= 0.0174    and param[18] <= 1884.95
#     paramOkay[19] = param[19] >= 0.0174    and param[19] <= 1884.95
#     paramOkay[20] = param[20] >= 0.0174    and param[20] <= 1884.95
#     paramOkay[21] = param[21] >= 0.0000001 and param[21] <= 1000
#     paramOkay[22] = param[22] >= 0.0000001 and param[22] <= 1000
#     paramOkay[23] = param[23] >= 0.0000001 and param[23] <= 1000
#     paramOkay[24] = param[24] >= 0.0000001 and param[24] <= 1000

#     allParamOk = True
#     errorParam = list()
#     for i in range(22):
#         allParamOk &= paramOkay[i]
#         if paramOkay[i] == False:
#             errorParam.append(i)
#     if errorParam != []:
#         print("Error Parameter No.", errorParam)
#     # print("Parameter Okay =", allParamOk)
    
#     return allParamOk

def actionCMD(index, value):
    if connectState == True:
        cmdOut = "/ " + str(index) + " " + str(value) + "\n"
        print(cmdOut, end='')
        put2TextBox(cmdOut)
        ser.write(cmdOut.encode('utf_8'))

def MotorEn():
    global MotorEnState

    if connectState == True:
        if MotorEnState == True:
            btnMotor.configure(text="Enable", state="normal")
            actionCMD(26, 0)
            MotorEnState = False
        else:
            btnMotor.configure(text="Disable", state="normal")
            actionCMD(26, 1)
            MotorEnState = True

def EnterControlMode():
    actionCMD(32, 1)
    btnRead.configure(state="disable")
    btnWrite.configure(state="disable")
    # btnRebt.configure(state="disable")
    # btnMotor.configure(text="Enable", state="disable")
    btnCtrMod.configure(state="disable")
    btnOPdiv1.configure(state="disable")
    btnOPdiv2.configure(state="disable")
    btnCLdiv1.configure(state="disable")
    btnCLdiv2.configure(state="disable")
    btnGetAng.configure(state="disable")
    btnGetAngH.configure(state="disable")

def reboot():
    global MotorEnState

    actionCMD(30, 0)
    btnMotor.configure(text="Enable", state="normal")
    MotorEnState = False
    
    btnRead.configure(state="normal")
    btnWrite.configure(state="normal")
    btnCtrMod.configure(state="normal")
    btnOPdiv1.configure(state="normal")
    btnOPdiv2.configure(state="normal")
    btnCLdiv1.configure(state="normal")
    btnCLdiv2.configure(state="normal")
    btnGetAng.configure(state="normal")
    btnGetAngH.configure(state="normal")

def readCMD(event):
    global cmdStr
    cmdStr = cmd.get()
    print(">", cmdStr)
    ser.write(cmdStr.encode('utf_8'))
    put2TextBox('>> ' + cmdStr + '\n')
    cmdEntry.delete(0, END)

def put2TextBox(text):
    textBox.configure(state="normal")
    textBox.insert(END, text)
    textBox.configure(state="disable")
    textBox.see("end")

def clear():
    print("clear")
    textBox.configure(state="normal")
    textBox.delete('1.0' , 'end')
    textBox.configure(state="disable")

def mainLoop():
    if connectState == True:
        # ser.flush()
        if ser.inWaiting() > 0:
            answer = ""
            answer_str = ""
            while ser.inWaiting() > 0:
                answer = ser.readline()
                answer_str += answer.decode()
            print(answer_str)
            put2TextBox(answer_str + '\n')

    root.after(100, mainLoop)

def main():
    global root
    global portCombo, btnCon, statusLabel
    global portChoice, rateChoice
    global textBox, cmdEntry, cmd
    global connectState, port
    global paramVar
    global btnRead, btnWrite, btnRebt
    global btnMotor, btnCtrMod, btnOPdiv1, btnOPdiv2
    global btnCLdiv1, btnCLdiv2, btnGetAng, btnGetAngH
    global MotorEnState

    root = Tk()
    root.title("BLDC driver config")
    root.geometry("+600+0")

    connectState = False
    MotorEnState = False

    # ------------------------ Config Connection -----------------------
    frmCfgSer = ttk.LabelFrame(root, text="Config Connection")
    frmCfgSer.grid(row=0, column=0, padx=5, pady=5)

    # row 0 port setting
    Label(frmCfgSer, text="COM Port").grid(row=0, column=0, padx=20)
    availablePort = serialList()
    portChoice = StringVar(value="Select port")
    portCombo = ttk.Combobox(frmCfgSer, textvariable=portChoice, values=availablePort)

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
    Label(frmCfgSer, text="baud rate").grid(row=1, column=0, padx=20)
    rateChoice = StringVar(value="Select baud rate")
    rateCombo = ttk.Combobox(frmCfgSer, textvariable=rateChoice, state="readonly")
    rateCombo["value"] = [9600, 115200, 1000000, 2000000]
    rateCombo.bind("<<ComboboxSelected>>", connectionSetted)
    rateCombo.grid(row=1, column=1)

    # row 2 button
    btnRefresh = Button(frmCfgSer, text="Refresh", command=refresh, width=10)
    btnRefresh.grid(row=0, column=2, padx=10)

    btnCon = Button(frmCfgSer, text="Connect", state="disable", command=makeConnect, width=10)
    btnCon.grid(row=1, column=2, padx=10)

    statusLabel = Label(frmCfgSer, text="status: disconnected", fg="#fc5203")
    statusLabel.grid(row=2, column=2, padx=20)

    # ------------------------ Config Parameter ------------------------
    frmParam = ttk.LabelFrame(root, text="Config Parameter")
    frmParam.grid(row=1, column=0, rowspan=2, padx=5, pady=5)

    paramVar = list()
    paramEntry = list()
    
    for i in range(25):
        paramVar.append(DoubleVar(value=0))
    
    for i in range(25):
        paramEntry.append(Entry(frmParam, textvariable=paramVar[i]))
        paramEntry[i].grid(row=i, column=1)

    Label(frmParam, text="Motor ID").grid(row=0, column=0, sticky='W')
    Label(frmParam, text="[1 ~ 254]").grid(row=0, column=2, sticky='W')
    
    Label(frmParam, text="Control Mode").grid(row=1, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 2]").grid(row=1, column=2, sticky='W')
    
    Label(frmParam, text="Voltage Source").grid(row=2, column=0, sticky='W')
    Label(frmParam, text="[5 ~ 26] volt").grid(row=2, column=2, sticky='W')

    Label(frmParam, text="Current Limit").grid(row=3, column=0, sticky='W')
    Label(frmParam, text="[0.1 ~ 8.5] amp").grid(row=3, column=2, sticky='W')
    
    Label(frmParam, text="Temperature Limit").grid(row=4, column=0, sticky='W')
    Label(frmParam, text="[30 ~ 80] celcius").grid(row=4, column=2, sticky='W')

    Label(frmParam, text="Motor Pole Pair").grid(row=5, column=0, sticky='W')
    Label(frmParam, text="[1 ~ 24]").grid(row=5, column=2, sticky='W')
    
    Label(frmParam, text="Motor Direction").grid(row=6, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 1]").grid(row=6, column=2, sticky='W')

    Label(frmParam, text="Rotor Offset CW").grid(row=7, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 16383]").grid(row=7, column=2, sticky='W')
    
    Label(frmParam, text="Rotor Offset CCW").grid(row=8, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 16383]").grid(row=8, column=2, sticky='W')

    Label(frmParam, text="Shaft Offset").grid(row=9, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 16383]").grid(row=9, column=2, sticky='W')

    Label(frmParam, text="Gear Ratio").grid(row=10, column=0, sticky='W')
    Label(frmParam, text="[0.001 ~ 1000]").grid(row=10, column=2, sticky='W')

    Label(frmParam, text="PWM Resolution").grid(row=11, column=0, sticky='W')
    Label(frmParam, text="[16 ~ 1024]").grid(row=11, column=2, sticky='W')
    
    Label(frmParam, text="Encoder Direction").grid(row=12, column=0, sticky='W')
    Label(frmParam, text="[0 ~ 1]").grid(row=12, column=2, sticky='W')

    Label(frmParam, text="Time Debug").grid(row=13, column=0, sticky='W')
    Label(frmParam, text="[0.5 ~ 15] sec").grid(row=13, column=2, sticky='W')
    
    Label(frmParam, text="Voltage Debug").grid(row=14, column=0, sticky='W')
    Label(frmParam, text="[10 ~ 100] %").grid(row=14, column=2, sticky='W')

    Label(frmParam, text="Resolution Debug").grid(row=15, column=0, sticky='W')
    Label(frmParam, text="[0.00174 ~ 2.617] rad").grid(row=15, column=2, sticky='W')
    
    Label(frmParam, text="Maximum Velocity").grid(row=16, column=0, sticky='W')
    Label(frmParam, text="[0.0174 ~ 1884.95] rad/sec").grid(row=16, column=2, sticky='W')

    Label(frmParam, text="Minimum Velocity").grid(row=17, column=0, sticky='W')
    Label(frmParam, text="[0.0174 ~ 1884.95] rad/sec").grid(row=17, column=2, sticky='W')
    
    Label(frmParam, text="Velocity Limit").grid(row=18, column=0, sticky='W')
    Label(frmParam, text="[0.0174 ~ 1884.95] rad/sec").grid(row=18, column=2, sticky='W')

    Label(frmParam, text="Acceleration Limit").grid(row=19, column=0, sticky='W')
    Label(frmParam, text="[0.0174 ~ 1884.95] rad/sec2").grid(row=19, column=2, sticky='W')

    Label(frmParam, text="Deceleration Limit").grid(row=20, column=0, sticky='W')
    Label(frmParam, text="[0.0174 ~ 1884.95] rad/sec2").grid(row=20, column=2, sticky='W')

    Label(frmParam, text="Position Control P Gain").grid(row=21, column=0, sticky='W')
    Label(frmParam, text="[0.0000001 ~ 1000]").grid(row=21, column=2, sticky='W')

    Label(frmParam, text="Position Control I Gain").grid(row=22, column=0, sticky='W')
    Label(frmParam, text="[0.0000001 ~ 1000]").grid(row=22, column=2, sticky='W')

    Label(frmParam, text="Velocity Control P Gain").grid(row=23, column=0, sticky='W')
    Label(frmParam, text="[0.0000001 ~ 1000]").grid(row=23, column=2, sticky='W')

    Label(frmParam, text="Velocity Control I Gain").grid(row=24, column=0, sticky='W')
    Label(frmParam, text="[0.0000001 ~ 1000]").grid(row=24, column=2, sticky='W')

    btnRead = Button(frmParam, text="Read EEPROM", width=13, command=readParam)
    btnRead.grid(row=25, column=0, padx=5, pady=5)

    btnWrite = Button(frmParam, text="Write EEPROM", width=13, command=writeParam)
    btnWrite.grid(row=25, column=1, padx=5, pady=5)

    btnRebt = Button(frmParam, text="Reboot", width=13, command=reboot)
    btnRebt.grid(row=25, column=2, padx=5, pady=5)

    # ----------------------------- Action -----------------------------
    frmAct = ttk.LabelFrame(root, text="Action")
    frmAct.grid(row=0, column=1, rowspan=2, padx=5, pady=5)
    
    # -----------------------------------------------------
    Label(frmAct, text="Motor").grid(row=0, column=0, padx=10, pady=3, sticky='W')
    
    btnMotor = Button(frmAct, text="Enable", width=13, command=MotorEn)
    btnMotor.grid(row=0, column=1, padx=10, pady=3)

    btnCtrMod = Button(frmAct, text="Control Mode", width=13, command=EnterControlMode)
    btnCtrMod.grid(row=0, column=2, padx=10, pady=3)
    # -----------------------------------------------------
    Label(frmAct, text="Open Loop Drive").grid(row=1, column=0, padx=10, pady=3, sticky='W')

    btnOPdiv1 = Button(frmAct, text="CW", width=13, command=lambda: actionCMD(27, 0))
    btnOPdiv1.grid(row=1, column=1, padx=10, pady=3)

    btnOPdiv2 = Button(frmAct, text="CCW", width=13, command=lambda: actionCMD(27, 1))
    btnOPdiv2.grid(row=1, column=2, padx=10, pady=3)

    # -----------------------------------------------------
    Label(frmAct, text="Close Loop Drive").grid(row=2, column=0, padx=10, pady=3, sticky='W')
    
    btnCLdiv1 = Button(frmAct, text="CW", width=13, command=lambda: actionCMD(28, 0))
    btnCLdiv1.grid(row=2, column=1, padx=10, pady=3)

    btnCLdiv2 = Button(frmAct, text="CCW", width=13, command=lambda: actionCMD(28, 1))
    btnCLdiv2.grid(row=2, column=2, padx=10, pady=3)

    # -----------------------------------------------------
    Label(frmAct, text="Rotor Alignment").grid(row=3, column=0, padx=10, pady=3, sticky='W')
    
    btnGetAng = Button(frmAct, text="Raw Angle", width=13, command=lambda: actionCMD(29, 0))
    btnGetAng.grid(row=3, column=1, padx=10, pady=3)
    
    btnGetAngH = Button(frmAct, text="Offset Angle", width=13, command=lambda: actionCMD(29, 1))
    btnGetAngH.grid(row=3, column=2, padx=10, pady=3)
 
    # ------------------------- Serial Monitor -------------------------
    frmSerMon = ttk.LabelFrame(root, text="Serial Monitor")
    frmSerMon.grid(row=2, column=1, padx=20, pady=5)

    textBox = Text(frmSerMon, width=40, heigh=28, state="disable")
    textBox.grid(row=0, column=0, columnspan=3, padx=5, pady=5)

    cmd = StringVar()
    cmdEntry = Entry(frmSerMon, textvariable=cmd, width=47, state="disable")
    cmdEntry.bind('<Return>', readCMD)
    cmdEntry.grid(row=1, column=0, columnspan=2, padx=2, pady=2)

    btnClear = Button(frmSerMon, text="Clear", command=clear)
    btnClear.grid(row=1, column=2, padx=2, pady=2)

    # -----------------------------------------------------
    disConnect()

    root.after(100, mainLoop)
    root.mainloop()

if __name__ == '__main__':
    main()
