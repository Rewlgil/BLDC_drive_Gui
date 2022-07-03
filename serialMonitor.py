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

def readCMD(event):
    global cmdStr
    cmdStr = cmd.get()

    if 'b' in cmdStr:
        cmd_bin_str = cmdStr.replace('b', '')
        cmd_bin = cmd_bin_str.split(" ")

        cmd_int = [int(s, 2) for s in cmd_bin]

    else:
        cmd_str_lis = cmdStr.split(" ")
        
        cmd_int = [int(s, 16) for s in cmd_str_lis]

        cmd_bin = [bin(i) for i in cmd_int]
        cmd_bin_str = " ".join(cmd_bin)

    cmd_hex = [hex(i) for i in cmd_int]
    cmd_hex_str = " ".join(cmd_hex)

    cmd_byte = bytearray(cmd_int)
    print(">>", cmd_hex_str)
    ser.write(cmd_byte)
    textBox.configure(state="normal")
    textBox.insert(END, '>> ' + cmd_hex_str + '\t' + cmd_bin_str + '\n')
    textBox.configure(state="disable")
    cmdEntry.delete(0, END)
    textBox.see("end")

def mainLoop():
    if connectState == True:
        # ser.flush()
        if ser.inWaiting() > 0:
            answer = ""
            ans_hex_str = ""
            ans_bin_str = ""
            while ser.inWaiting() > 0:
                answer = ser.read()
                ans_int = int.from_bytes(answer, byteorder='little')
                
                ans_hex = hex(ans_int)
                ans_hex_str += str(ans_hex) + ' '

                ans_bin = bin(ans_int)
                ans_bin_str += str(ans_bin) + ' '
            
            print(ans_hex_str, ans_bin, sep="\t")
            textBox.configure(state="normal")
            textBox.insert(END, ans_hex_str + '\t' + ans_bin_str + '\n')
            textBox.configure(state="disable")
            textBox.see("end")

    root.after(100, mainLoop)

def main():
    global root
    global portCombo, btnCon, statusLabel
    global portChoice, rateChoice
    global textBox, cmdEntry, cmd
    global connectState, port

    root = Tk()
    root.title("Serial Monitor")
    root.geometry("500x650+600+0")

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
    # rateChoice = StringVar(value="Select baud rate")
    rateChoice = StringVar()
    rateCombo = ttk.Combobox(textvariable=rateChoice, state="readonly")
    rateCombo["value"] = [9600, 115200, 1000000, 2000000]
    rateCombo.bind("<<ComboboxSelected>>", connectionSetted)
    rateCombo.current(0)
    rateCombo.grid(row=1, column=1)

    # row 2 button
    btnRefresh = Button(text="Refresh", command=refresh)
    btnRefresh.grid(row=0, column=2)

    btnCon = Button(text="Connect", command=makeConnect, state="disable")
    btnCon.grid(row=1, column=2)

    statusLabel = Label(text="status: disconnected", fg="#fc5203")
    statusLabel.grid(row=2, column=2)

    # row 3 ~ 4 serial monitor
    textBox = Text(width=60, heigh=30, state="disable")
    textBox.grid(row=3, column=0, columnspan=3)

    cmd = StringVar()
    cmdEntry = Entry(textvariable=cmd, width=53, state="disable")
    cmdEntry.bind('<Return>', readCMD)
    cmdEntry.grid(row=4, column=0, columnspan=3)

    connectionSetted("call")

    root.after(100, mainLoop)
    root.mainloop()

if __name__ == '__main__':
    main()