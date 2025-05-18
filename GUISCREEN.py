import tkinter
from numpy.lib.function_base import select
import serial
import queue
#import msvcrt
import time
import typing
import threading
import RPi.GPIO as GP
import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import numpy as np

# set up window
window = tk.Tk(className=" GUI ")
window.attributes("-fullscreen", True)  



GP.setmode(GP.BCM)
GP.setup(0, GP.OUT)
global trigger

# create all of the main containers
topFrameL = Frame(window, height=20, bg="#14161A", bd=0)
topFrameL.grid(row=0, column=0, sticky="nsew")
topFrameR = Frame(window, height=20, bg="#14161A", bd=0)
topFrameR.grid(row=0, column=1, sticky="nsew")

menuFrame = Frame(window, height=750, width=700, bg="#292C33", bd=0)
#shotsFrame = Frame(menuFrame, height=400, width=730, bg="#404040", bd=0)

#Shots confirm Frames
sCFrameLeft = Frame(menuFrame, height=480, width=285, bg="#292C33", bd=0)
sCFrameRight =  Frame(menuFrame, height=480, width=555, bg="#292C33", bd=0)

window.wm_attributes('-alpha', 0.2) 
var = IntVar()

#Selection===================
selectedDrink = "Test"
selDrink = ""
selAmount = 0

#Create clock
def clock():
    hour = time.strftime("%H")
    min = time.strftime("%M")
    sec = time.strftime("%S")

    t_label.config(text=hour + ":" + min + ":" + sec )
    t_label.after(1000, clock)


def SelectedAmount():
    return

def RGBAImage(path, width, height):
    image = Image.open(path).convert("RGBA")

    res_image = image.resize((width, height), Image.ANTIALIAS)
    return ImageTk.PhotoImage(res_image)

#==================TransparencyConverter=========================
def convert_pillow(image):
    #print('[DEBUG] convert_pillow')
    
    # Load the pizels into memory
    pixels = image.load()
    
    # For each pixel in the image
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            # If the pixel is white
            if pixels[i, j] == (255, 255, 255, 255):
                # Make it transparent
                pixels[i, j] = (255, 255, 255, 0)

    return image
    
def convert_numpy(image):
    #print('[DEBUG] convert_numpy')
    import numpy as np

    # convert pillow.Image to numpy.array
    array = np.array(image)  
    
    #mask = np.all(array == [255, 255, 255, 255], axis=-1)  # png without artefacts
    mask = np.all(array >= [230, 230, 230, 255], axis=-1)  # jpg with artefacts
    array[ mask ] = [255, 255, 255, 0]

    # convert numpy.array to pillow.Image
    image = Image.fromarray(array)
    
    return image

# --- main ---
def RGBAConverter(filename, width, height):
    #filename = "/home/pi/Desktop/SB/SymbolsBtn/Shots1A.png"
    image = Image.open(filename).convert("RGBA")

    #image = convert_pillow(image)
    image = convert_numpy(image)

    # resize after changing color - because resize creates new artefacts
    image = image.resize((width, height), Image.LANCZOS)

    # Save the now transparent image:
    image.save("new_image.png", format="png")

    tk_image = ImageTk.PhotoImage(image)
    return tk_image

#==================TransparencyConverter=========================

#Create Style for radioButtons
# neededColor = "#292C33"
# window.configure(bg=neededColor)
# radioStyle = ttk.Style()
# radioStyle.configure('SB.TRadiobutton', background=neededColor)

#create label
t_label = Label(topFrameL, text="Old Text", anchor=CENTER, font=("Helvetica", 20), bg="#14161A", fg="#efefef")
t_label.grid(row=0, sticky="W")



filenameShots1 = "/home/pi/Desktop/SB/SymbolsBtn/Shots1A.png"
filenameShots2 = "/home/pi/Desktop/SB/SymbolsBtn/Shots2A.png"
filenameShots3 = "/home/pi/Desktop/SB/SymbolsBtn/Shots3A.png"
cola = "/home/pi/Desktop/SB/SymbolsBtn/Cola.png"
sprite = "/home/pi/Desktop/SB/SymbolsBtn/Sprite.png"
bacardiCola = "/home/pi/Desktop/SB/SymbolsBtn/BacCola.png"
bacardiSprite = "/home/pi/Desktop/SB/SymbolsBtn/BacSprite.png"
absoluteCola = "/home/pi/Desktop/SB/SymbolsBtn/AbsCola.png"
absoluteSprite = "/home/pi/Desktop/SB/SymbolsBtn/AbsSprite.png"
licorCola = "/home/pi/Desktop/SB/SymbolsBtn/LicCola.png"
licorSprite = "/home/pi/Desktop/SB/SymbolsBtn/LicSprite.png"
low = "/home/pi/Desktop/SB/SymbolsBtn/LowAmount_1.png"
middel = "/home/pi/Desktop/SB/SymbolsBtn/MiddelAmount_1.png"
high = "/home/pi/Desktop/SB/SymbolsBtn/HighAmount_1.png"
low_selected = "/home/pi/Desktop/SB/SymbolsBtn/LowAmount_Selected.png"
middel_selected = "/home/pi/Desktop/SB/SymbolsBtn/MiddelAmount_Selected.png"
high_Selected = "/home/pi/Desktop/SB/SymbolsBtn/HighAmount_Selected.png"
showCola = "/home/pi/Desktop/SB/SymbolsBtn/ShowCola.png"
showSprite = "/home/pi/Desktop/SB/SymbolsBtn/ShowSprite.png"
showBaco = "/home/pi/Desktop/SB/SymbolsBtn/ShowBaco.png"
showBaSprite = "/home/pi/Desktop/SB/SymbolsBtn/ShowBaSprite.png"
showAbsCola = "/home/pi/Desktop/SB/SymbolsBtn/ShowAbsCola.png"
showAbsSprite = "/home/pi/Desktop/SB/SymbolsBtn/ShowAbsSprite.png"
showLicCola = "/home/pi/Desktop/SB/SymbolsBtn/ShowLicCola.png"
showLicSprite = "/home/pi/Desktop/SB/SymbolsBtn/ShowLicSprite.png"
bevestigen = "/home/pi/Desktop/SB/SymbolsBtn/BevestigBtn.png"

shots1Image = RGBAConverter(filenameShots1, 200, 210)
shots2Image = RGBAConverter(filenameShots2, 200, 210)
shots3Image = RGBAConverter(filenameShots3, 200, 210)
colaImg = RGBAConverter(cola, 170, 170)
spriteImg = RGBAConverter(sprite, 170, 170)
bacardiColaImg = RGBAConverter(bacardiCola, 170, 170)
bacardiSpriteImg = RGBAConverter(bacardiSprite, 170, 170)
absoluteColaImg = RGBAConverter(absoluteCola, 170, 170)
absoluteSpriteImg = RGBAConverter(absoluteSprite, 170, 170)
licorColaImg = RGBAConverter(licorCola, 170, 170)
licorSpriteImg = RGBAConverter(licorSprite, 170, 170)
lowAmountImg = RGBAImage(low, 150, 155)
middelAmountImg = RGBAImage(middel, 150, 155)
highAmountImg = RGBAImage(high, 150, 155)
lowAmountSelectedImg = RGBAImage(low_selected, 150, 155)
midAmountSelectedImg = RGBAImage(middel_selected, 150, 155)
highAmountSelected = RGBAImage(high_Selected, 150, 155)
bevestigImg = RGBAImage(bevestigen, 510, 150 )
showColaImg = RGBAImage(showCola, 290, 455)
showSpriteImg = RGBAImage(showSprite, 290, 455)
showBacoImg = RGBAImage(showBaco, 290, 455)
showBaSpriteImg = RGBAImage(showBaSprite, 290, 455)
showAbsColaImg = RGBAImage(showAbsCola, 290, 455)
showAbsSpriteImg = RGBAImage(showAbsSprite, 290, 455)
showLicColaImg = RGBAImage(showLicCola, 290, 455)
showLicSpriteImg = RGBAImage(showLicSprite, 290, 455)

#Create Buttons
btnCola = Button(menuFrame, image=colaImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank1"))
btnSprite = Button(menuFrame, image=spriteImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0,borderwidth=0, command=lambda: showButtons("Drank2"))
btnBacCola = Button(menuFrame, image=bacardiColaImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank3"))
btnBacSprite = Button(menuFrame, image=bacardiSpriteImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank4"))
btnAbsCola = Button(menuFrame, image=absoluteColaImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0,borderwidth=0, command=lambda: showButtons("Drank5"))
btnAbsSprite = Button(menuFrame, image=absoluteSpriteImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank6"))
btnLicCola = Button(menuFrame, image=licorColaImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank7"))
btnLicSprite = Button(menuFrame, image=licorSpriteImg, activebackground="#292C33",bg="#292C33",
    highlightthickness=0, borderwidth=0, command=lambda: showButtons("Drank8"))
returnBtn = Button(topFrameR, text="Terug", bg="#353434", fg="#efefef",
    highlightthickness=0, command=lambda: showButtons("main"))
shot1Btn = Button(menuFrame,image=shots1Image, highlightthickness=0, activebackground="#292C33",bg="#292C33", borderwidth=0, height=200, width=210)
shot2Btn = Button(menuFrame,image=shots2Image, highlightthickness=0, activebackground="#292C33",bg="#292C33", borderwidth=0, height=200, width=210)
shot3Btn = Button(menuFrame,image=shots3Image, highlightthickness=0, activebackground="#292C33",bg="#292C33", borderwidth=0, height=200, width=210)
lowAmountBtn = Radiobutton(sCFrameRight,image=lowAmountImg,variable=selAmount, value=1, highlightthickness=0,indicatoron=0, takefocus=0, 
    activebackground="#292C33",bg="#292C33", highlightcolor="#292C33",borderwidth=0, highlightbackground="#292C33", selectcolor="#292C33",height=160, width=165, selectimage=lowAmountSelectedImg)
midAmountBtn = Radiobutton(sCFrameRight,image=middelAmountImg,variable=selAmount, value=2, 
    highlightthickness=0,indicatoron=0 ,activebackground="#292C33",bg="#292C33", selectcolor="#292C33",borderwidth=0, height=160, width=165, selectimage=midAmountSelectedImg)
highAmountBtn = Radiobutton(sCFrameRight,image=highAmountImg, variable=selAmount, value=3, 
    highlightthickness=0, indicatoron=0 ,activebackground="#292C33",bg="#292C33", selectcolor="#292C33",borderwidth=0, height=160, width=165, selectimage=highAmountSelected)
BevestigBtn = Button(sCFrameRight,image=bevestigImg, highlightthickness=0, activebackground="#292C33",bg="#292C33", borderwidth=0 , height=150, width=510, command=lambda: confirmedOrder())

drinkDisplayCola = Label(sCFrameLeft, image=showColaImg, bg="#292C33")
drinkDisplaySprite = Label(sCFrameLeft, image=showSpriteImg, bg="#292C33")
drinkDisplayBaco = Label(sCFrameLeft, image=showBacoImg, bg="#292C33")
drinkDisplayBaSprite = Label(sCFrameLeft, image=showBaSpriteImg, bg="#292C33")
drinkDisplayAbsCola = Label(sCFrameLeft, image=showAbsColaImg, bg="#292C33")
drinkDisplayAbsSprite = Label(sCFrameLeft, image=showAbsSpriteImg, bg="#292C33")
drinkDisplayLicCola= Label(sCFrameLeft, image=showLicColaImg, bg="#292C33")
drinkDisplayLicSprite = Label(sCFrameLeft, image=showLicSpriteImg, bg="#292C33")


window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.rowconfigure(0, weight=0)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)

testCanvas = Canvas(window, height=300, width=300 ,bg="#353434", highlightthickness=0)


#Grid
menuFrame.grid(row=1, column=0,columnspan=4, rowspan=4, sticky="nsew")
btnCola.grid(row=1, column=0,pady=20, padx=15, sticky="nsew")
btnSprite.grid(row=2, column=0,pady=20, padx=15, sticky="nsew")
btnBacCola.grid(row=1, column=1,pady=20, padx=15, sticky="nsew")
btnBacSprite.grid(row=2, column=1, pady=20, padx=15,sticky="nsew")
btnAbsCola.grid(row=1, column=2,pady=20, padx=15, sticky="nsew")
btnAbsSprite.grid(row=2, column=2,pady=20, padx=15, sticky="nsew")
btnLicCola.grid(row=1, column=3,pady=20, padx=15, sticky="nsew")
btnLicSprite.grid(row=2, column=3,pady=20, padx=15, sticky="nsew")


#List of buttons
#button_list = [button_1, button_2, button_3, button_4, button_5, button_6,button_7,button_8]

#Row & Collumn counter
row_number = 0

def showButtons(menu):
    if menu == "main":
        forgetAllWidgets()
        retrieveWidgetMain()
        return
    elif menu == "Drank1":
        forgetAllWidgetsMain()
        
        drank_1_Select()
        return
    elif menu == "Drank2":
        forgetAllWidgetsMain()
        drank_2_Select()
        return
    elif menu == "Drank3":
        forgetAllWidgetsMain()
        drank_3_Select()
        return
    elif menu == "Drank4":
        forgetAllWidgetsMain()
        drank_4_Select()
        return
    elif menu == "Drank5":
        forgetAllWidgetsMain()
        drank_5_Select()
        return
    elif menu == "Drank6":
        forgetAllWidgetsMain()
        drank_6_Select()
        return
    elif menu == "Drank7":
        forgetAllWidgetsMain()
        drank_7_Select()
        return
    elif menu == "Drank8":
        forgetAllWidgetsMain()
        drank_8_Select()
        return

def drank_1_Select():
    global selectedDrink
    selectedDrink = "Cola"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayCola.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return 

def drank_2_Select():
    global selectedDrink
    selectedDrink = "Sprite"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplaySprite.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_3_Select():
    global selectedDrink
    selectedDrink = "Baco"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayBaco.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_4_Select():
    global selectedDrink
    selectedDrink = "BaSprite"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayBaSprite.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_5_Select():
    global selectedDrink
    selectedDrink = "AbsCola"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayAbsCola.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_6_Select():
    global selectedDrink
    selectedDrink = "AbsSprite"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayAbsSprite.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_7_Select():
    global selectedDrink
    selectedDrink = "LicCola"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayLicCola.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def drank_8_Select():
    global selectedDrink
    selectedDrink = "LicSprite"

    menuFrame.grid(row=1, column=0,columnspan=2, rowspan=4, sticky="nsew")
    returnBtn.grid(row=0, column=0,columnspan=3 ,sticky=E)
    sCFrameLeft.grid(row=0, column=0, sticky=NSEW)
    sCFrameRight.grid(row=0, column=1, sticky=NSEW)
    drinkDisplayLicSprite.grid(row=0, column=0, sticky=NSEW)
    shotsLoader() 
    return

def shotsLoader():
    lowAmountBtn.grid(row=2, column=0 , pady=10)
    midAmountBtn.grid(row=2, column=1, pady=10)
    highAmountBtn.grid(row=2, column=2, pady=10)
    BevestigBtn.grid(row=3 , rowspan=4, column=0, pady=100,columnspan=3) 
    lowAmountBtn.select()
    return



def confirmedOrder():
    GP.cleanup()
    print(selectedDrink + " ")

    #setup selected drink
    if selectedDrink == "Cola":
        GP.setmode(GP.BCM)
        GP.setup(18, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(18, 1000)
        trigger.start(75.0)
        print("start")
        trigger.stop()
        print("stopped")
        #Activate Timer
        #time.sleep(3)
        GP.cleanup()
        return
    elif selectedDrink == "Sprite":
        GP.setmode(GP.BCM)
        GP.setup(23, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(23, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "Baco":
        GP.setmode(GP.BCM)
        GP.setup(24, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(24, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(18, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(18, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "BaSprite":
        GP.setmode(GP.BCM)
        GP.setup(24, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(24, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(23, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(23, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "AbsCola":
        GP.setmode(GP.BCM)
        GP.setup(17, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(17, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(18, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(18, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "AbsSprite":
        GP.setmode(GP.BCM)
        GP.setup(17, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(17, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(23, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(23, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "LicCola":
        GP.setmode(GP.BCM)
        GP.setup(27, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(27, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(18, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(18, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    elif selectedDrink == "LicSprite":
        GP.setmode(GP.BCM)
        GP.setup(27, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(27, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()

        #Second Drink
        GP.setmode(GP.BCM)
        GP.setup(23, GP.OUT)

        #Activate trigger
        trigger = GP.PWM(23, 1000)
        trigger.start(100.0)

        #Activate Timer
        time.sleep(3)
        trigger.stop()
        GP.cleanup()
        return
    return

def forgetAllWidgetsMain():
    btnCola.grid_forget()
    btnSprite.grid_forget()
    btnBacCola.grid_forget()
    btnBacSprite.grid_forget()
    btnAbsCola.grid_forget()
    btnAbsSprite.grid_forget()
    btnLicCola.grid_forget()
    btnLicSprite.grid_forget()
    return

def forgetAllWidgets():
    btnCola.grid_forget()
    btnSprite.grid_forget()
    btnBacCola.grid_forget()
    btnBacSprite.grid_forget()
    btnAbsCola.grid_forget()
    btnAbsSprite.grid_forget()
    btnLicCola.grid_forget()
    btnLicSprite.grid_forget()
    returnBtn.grid_forget()
    menuFrame.grid_forget()
    #shotsFrame.grid_forget()
    shot1Btn.grid_forget()
    shot2Btn.grid_forget()
    shot3Btn.grid_forget()
    lowAmountBtn.grid_forget()
    midAmountBtn.grid_forget()
    highAmountBtn.grid_forget()
    sCFrameLeft.grid_forget()
    sCFrameRight.grid_forget()
    BevestigBtn.grid_forget()
    drinkDisplayCola.grid_forget()
    drinkDisplaySprite.grid_forget()
    drinkDisplayBaco.grid_forget()
    drinkDisplayBaSprite.grid_forget()
    drinkDisplayAbsCola.grid_forget()
    drinkDisplayAbsSprite.grid_forget()
    drinkDisplayLicCola.grid_forget()
    drinkDisplayLicSprite.grid_forget()
    return

def retrieveWidgetMain():
    menuFrame.grid(row=1, column=0,columnspan=4, rowspan=4, sticky="nsew")
    btnCola.grid(row=1, column=0,pady=20, padx=15, sticky="nsew")
    btnSprite.grid(row=2, column=0,pady=20, padx=15, sticky="nsew")
    btnBacCola.grid(row=1, column=1,pady=20, padx=15, sticky="nsew")
    btnBacSprite.grid(row=2, column=1, pady=20, padx=15,sticky="nsew")
    btnAbsCola.grid(row=1, column=2,pady=20, padx=15, sticky="nsew")
    btnAbsSprite.grid(row=2, column=2,pady=20, padx=15, sticky="nsew")
    btnLicCola.grid(row=1, column=3,pady=20, padx=15, sticky="nsew")
    btnLicSprite.grid(row=2, column=3,pady=20, padx=15, sticky="nsew")
    return

def deleteMainBtn():
    btnCola.destroy()
    btnSprite.destroy()
    btnBacCola.destroy()
    btnBacSprite.destroy()
    btnAbsCola.destroy()
    btnAbsSprite.destroy()
    btnLicCola.destroy()
    btnLicSprite.destroy()
    return



clock()
window.mainloop()

