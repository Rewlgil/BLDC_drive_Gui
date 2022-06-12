from tkinter import *
from tkinter import ttk
import serialList
import serial
import time

def disconnect():
    print("disconnected")
    ser.close()
    serConnection = False
    btnRefresh["state"] = "normal"

def makeConnection():
    global ser, serConnection, btnRefresh, btnCon, portCombo, rateCombo
    print("Connectted to ", port, " baud rate =", rate)
    ser = serial.Serial(port, rate, timeout=0.1)
    if ser.is_open == False:
        ser.open()
    
    serConnection = True
    # btnRefresh["state"] = "disable"
    portCombo["state"] = "disable"
    rateCombo["state"] = "disable"
    btnRefresh.configure(state="disable")
    btnCon.configure(text="Disconnect", command="disconnect")

    time.sleep(1)
    ser.write(b"Hello Arduino")

def connectBtn(event):
    global port, rate, serConnection, btnRefresh, btnCon
    port = portChoice.get()
    rate = rateChoice.get()
    print("port =", port, " baud rate =", rate)

    btnCon = Button(text="Connect", command=makeConnection)
    btnCon.grid(row=2, column=1, sticky=E)
    if rate == "Select baud rate" or port == "No availabel port" or port == "Select port":
        btnCon.configure(state="disable")
    else:
        btnCon.configure(state="normal")
        rate = int(rate)

    if serConnection == False:
        btnRefresh = Button(text="Refresh", command=refresh, state="normal")
    btnRefresh.grid(row=2, column=1, sticky=W)

def selectPort():
    global portChoice, portCombo
    availablePort = serialList.serial_ports()

    Label(root, text="COM Port").grid(row=0, column=0)

    if availablePort == []:
        print("no available port")
        portChoice = StringVar(value="No availabel port")
        portCombo = ttk.Combobox(textvariable=portChoice, values=availablePort, state="disable")
    elif len(availablePort) == 1:
        print("found", availablePort)
        portChoice = StringVar(value="Select port")
        portCombo = ttk.Combobox(textvariable=portChoice, values=availablePort, state="readonly")
        portCombo.current(0)
    else:
        print("found", availablePort)
        portChoice = StringVar(value="Select port")
        portCombo = ttk.Combobox(textvariable=portChoice, values=availablePort, state="readonly")

    portCombo.grid(row=0, column=1)
    portCombo.bind("<<ComboboxSelected>>", connectBtn)

def selectRate():
    global rateChoice, rateCombo

    Label(root, text="baud rate").grid(row=1, column=0)
    rateChoice = StringVar(value="Select baud rate")
    rateCombo = ttk.Combobox(textvariable=rateChoice, state="readonly")
    rateCombo["value"] = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 31250, 38400, 57600, 115200]
    rateCombo.grid(row=1, column=1)
    rateCombo.bind("<<ComboboxSelected>>", connectBtn)

def refresh():
    print("Refresh")
    selectPort()
    selectRate()
    connectBtn("call")

#-------------------------------------------------------------------------------------------
def loop():
    #...
    root.after(100, loop)

def main():
    global root, serConnection
    serConnection = False
    
    root = Tk()
    root.title("BLDC driver config")

    refresh()
    root.after(100, loop)
    root.mainloop()
    print("End of main")
    if serConnection == True:
        ser.close()

if __name__ == '__main__':
    main()
    