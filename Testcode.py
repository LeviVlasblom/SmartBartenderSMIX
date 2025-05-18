import serial
import time
import typing
import threading
import tkinter as tk
from tkinter import *
from tkinter import StringVar, IntVar, BooleanVar

# start serial communication
#arduinoPort = serial.Serial('/dev/cu.usbmodem14201', baudrate=9600,
                            #timeout=1)  # create serial port (arduinoPort) and timeout if no data received for 1 second
time.sleep(1)

# set up window
window = tk.Tk(className=" GUI ")
window.attributes("-fullscreen", True)

# set up window panels
menuFrame = Frame(window, width=(800/3), height=480, bg="#2b2b2b", bd=0)
menuFrame.pack_propagate(0)
menuFrame.pack(side=LEFT)
buttonFrame = Frame(window,
                    width=(800/3), height=480, bg="#1f1f1f")
buttonFrame.pack_propagate(0)
buttonFrame.pack(side=LEFT)
buttonFrame2 = Frame(window, width=(800/3), height=480, bg="#1f1f1f")
buttonFrame2.pack_propagate(0)
buttonFrame2.pack(side=LEFT)

# create menu buttons
verlichtingMenuButton = tk.Button(menuFrame, text="Verlichting", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: showButtons("verlichting")).pack(fill=tk.X)
klimaatMenuButton = tk.Button(menuFrame, text="Klimaat", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: showButtons("klimaat")).pack(fill=tk.X)
bezoekersMenuButton = tk.Button(menuFrame, text="Bezoekers", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: showButtons("bezoekers")).pack(fill=tk.X)
refreshButton = tk.Button(menuFrame, text="Refresh data", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: serialDataRequest()).pack(fill=tk.X)

# create logo
#logo = PhotoImage(file="Logobitmap.gif")
#quitButton = Button(menuFrame, image=logo, anchor=S, highlightthickness=0, command=lambda: quitWindow()).pack()
def quitWindow():
    window.quit()

# user settable variables
lightState = BooleanVar()
lightState.set(False)
setTemperature = IntVar()
setTemperature.set(0)

# real world variables
currentTemperature = IntVar()
currentTemperature.set(0)
currentHumidity = IntVar()
currentHumidity.set(0)
currentVisitors = IntVar()
currentVisitors.set(0)

# serial temperature set commands
def serialTempDown():
    setTemperature.set(setTemperature.get() - 1)
    command = "SETT" + str(setTemperature.get())
    arduinoPort.write(command.encode())
    print("Temperature set down to ", setTemperature.get())
    temperatureSetCanvas.itemconfig(temperatureSetValue, text=setTemperature.get())
    return

def serialTempUp():
    setTemperature.set(setTemperature.get() + 1)
    command = "SETT" + str(setTemperature.get())
    arduinoPort.write(command.encode())
    print("Temperature set up to ", setTemperature.get())
    temperatureSetCanvas.itemconfig(temperatureSetValue, text=setTemperature.get())
    return

# serial light set command
def serialLightSwitch():
    if lightState.get():
        lightState.set(False)
        arduinoPort.write("SETLL".encode())
        print("Light switched off.")
        lightStateCanvas.itemconfig(lightStateValue, text="Uit")
    elif not lightState.get():
        lightState.set(True)
        arduinoPort.write("SETLH".encode())
        print("Light switched on.")
        lightStateCanvas.itemconfig(lightStateValue, text="Aan")
    return


# serial data request commands
def serialDataRequest():
    arduinoPort.write("datarequest".encode())
    time.sleep(1)
    # arduino programmer werkt nu niet op Mac OS dus moet handmatig getest worden
    # als de data zoals hieronder binnen komt is het oke
    # data = arduinoPort.readline()  # _xxx_xxx_xxx = _temp_humi_visi = _123_567_9 10 11
    data = "_031_061_031"
    print("Received data is ", data)
    currentTemperature.set(int(data[1:4]))
    currentHumidity.set(int(data[5:8]))
    currentVisitors.set(int(data[9:12]))
    print("Current temperature is ", currentTemperature.get())
    print("Current humidity is ", currentHumidity.get())
    print("Current visitors is ", currentVisitors.get())
    configureVisitorAlarmBackground()
    configureHumidityAlarmBackground()
    configureTemperatureAlarmBackground()



# set up GUI
def showButtons(menu):
    if menu == "verlichting":
        forgetAllWidgets()
        showLightingButtons()

    elif menu == "klimaat":
        forgetAllWidgets()
        showTemperatureSetButton()
        showTemperatureAlarm()
        showHumidityAlarm()

    elif menu == "bezoekers":
        forgetAllWidgets()
        #showVisitorsButtons()
        showVisitorsAlarm()
        #time.sleep(1)
        #currentVisitors.set(currentVisitors.get() + 1)
        #visitorsAlarmCanvas.itemconfig(visitorsValue, text=currentVisitors.get())
        #time.sleep(2)
        #currentVisitors.set(currentVisitors.get() + 10)
        #visitorsAlarmCanvas.itemconfig(visitorsValue, text=currentVisitors.get())


# create and set up user buttons
lightStateCanvas = Canvas(buttonFrame, width=250, height=220, bg="#353434", highlightthickness=0)
lightStateHeader = lightStateCanvas.create_text(125, 20, fill="#efefef", font=("Purisa", 15), text="Sfeerverlichting")
lightStateValue = lightStateCanvas.create_text(125, 110, fill="#efefef", font=("Purisa", 50), text="Undefined")

lightSwitchButton = tk.Button(buttonFrame, text="switchLight", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: serialLightSwitch())
def showLightingButtons():
    if lightState.get() == 1:
        state = "Aan"
    elif lightState.get() == 0:
        state = "Uit"
    lightStateCanvas.itemconfig(lightStateValue, text=state)
    lightStateCanvas.pack(padx=13, pady=13, anchor=NW)
    lightSwitchButton.pack(padx=13, pady=13, fill=tk.X)
    return

temperatureSetCanvas = Canvas(buttonFrame2, width=250, height=220, bg="#353434", highlightthickness=0)
temperatureSetHeader = temperatureSetCanvas.create_text(125, 20, fill="#efefef", font=("Purisa", 15), text="Instelling temperatuur")
temperatureSetValue = temperatureSetCanvas.create_text(125, 110, fill="#efefef", font=("Purisa", 50), text=setTemperature.get())
temperatureSetCanvas.create_polygon(125, 40, 157, 72, 93, 72, fill="#0a84ff")
temperatureSetCanvas.create_polygon(125, 212, 157, 180, 93, 180, fill="#0a84ff")

temperatureUpButton = tk.Button(buttonFrame2, text="tempUp", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: serialTempUp())
temperatureDownButton = tk.Button(buttonFrame2, text="tempUp", bg="#353434", fg="#efefef", height=5,
                                highlightthickness=0, command=lambda: serialTempDown())
def showTemperatureSetButton():
    temperatureSetCanvas.pack(padx=13, pady=13, anchor=NW)
    temperatureUpButton.pack(padx=13, pady=13, fill=tk.X)
    temperatureDownButton.pack(padx=13, pady=13, fill=tk.X)
    return


# create and set up alarm panels
temperatureAlarmCanvas = Canvas(buttonFrame, width=250, height=220, bg="#353434", highlightthickness=0)
temperatureHeader = temperatureAlarmCanvas.create_text(125, 20, fill="#efefef", font=("Purisa", 15), text="Temperatuur")
temperatureValue = temperatureAlarmCanvas.create_text(125, 110, fill="#efefef", font=("Purisa", 50), text=currentTemperature.get())
def showTemperatureAlarm():
    temperatureAlarmCanvas.itemconfig(temperatureValue, text=currentTemperature.get())
    configureTemperatureAlarmBackground()
    temperatureAlarmCanvas.pack(padx=13, pady=13, anchor=NW)
    return

def configureTemperatureAlarmBackground():
    temperatureAlarmCanvas.itemconfig(temperatureValue, text=currentTemperature.get())
    if currentTemperature.get() > 29:
        temperatureAlarmCanvas.config(bg="#ff453a")
    else:
        temperatureAlarmCanvas.config(bg="#353434")


humidityAlarmCanvas = Canvas(buttonFrame, width=250, height=220, bg="#353434", highlightthickness=0)
humidityHeader = humidityAlarmCanvas.create_text(125, 20, fill="#efefef", font=("Purisa", 15), text="Luchtvochtigheid")
humidityValue = humidityAlarmCanvas.create_text(125, 110, fill="#efefef", font=("Purisa", 50), text=currentHumidity.get())
def showHumidityAlarm():
    humidityAlarmCanvas.itemconfig(humidityValue, text=currentHumidity.get())
    configureHumidityAlarmBackground()
    humidityAlarmCanvas.pack(padx=13, pady=0, anchor=NW)
    return

def configureHumidityAlarmBackground():
    humidityAlarmCanvas.itemconfig(humidityValue, text=currentHumidity.get())
    if currentHumidity.get() > 60:
        humidityAlarmCanvas.config(bg="#ff453a")
    else:
        humidityAlarmCanvas.config(bg="#353434")


visitorsAlarmCanvas = Canvas(buttonFrame, width=250, height=220, bg="#353434", highlightthickness=0)
visitorsHeader = visitorsAlarmCanvas.create_text(125, 20, fill="#efefef", font=("Purisa", 15), text="Aantal bezoekers")
visitorsValue = visitorsAlarmCanvas.create_text(125, 110, fill="#efefef", font=("Purisa", 50), text=currentVisitors.get())
def showVisitorsAlarm():
    visitorsAlarmCanvas.itemconfig(visitorsValue, text=currentVisitors.get())
    configureVisitorAlarmBackground()
    visitorsAlarmCanvas.pack(padx=13, pady=13, anchor=NW)
    return

def configureVisitorAlarmBackground():
    visitorsAlarmCanvas.itemconfig(visitorsValue, text=currentVisitors.get())
    if currentVisitors.get() > 29:
        visitorsAlarmCanvas.config(bg="#ff453a")
    else:
        visitorsAlarmCanvas.config(bg="#353434")


# create forget widget function
def forgetAllWidgets():
    lightStateCanvas.forget()
    lightSwitchButton.forget()
    temperatureSetCanvas.forget()
    temperatureAlarmCanvas.forget()
    temperatureUpButton.forget()
    temperatureDownButton.forget()
    humidityAlarmCanvas.forget()
    visitorsAlarmCanvas.forget()
    return


def serialLoop():
    while True:
        serialDataRequest()
        time.sleep(1)

#serialThread = threading.Thread(target=serialLoop())
#serialThread.start()
#serialThread.join()
window.mainloop()
#window.quit()

