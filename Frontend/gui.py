"""
Main window gui


"""

import Tkinter
from Tkinter import *
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from controller import RotorController
import constant
rc = RotorController()


def _quit():
	print 'fire'
	if rc.statusAZ != constant.MotionStatus[4]:
		rc.disconnect()
	root.quit()     # stops mainloop
	root.destroy()  # this is necessary on Windows to prevent

def _connect():
	print rc.statusAZ

	if rc.statusAZ == constant.MotionStatus[4]:
		line = rc.connect("/dev/ttyACM0")
		ConnectBtnStr.set("Disconnect")
	elif rc.statusAZ != constant.MotionStatus[4]:
		rc.disconnect()
		ConnectBtnStr.set("Connect")
	updateStatus()

def buildGUI():
	root.protocol("WM_DELETE_WINDOW",_quit)
	setupLabelVariables()
	buildControlFrame()
	buildSkyPlot()

def setupLabelVariables(): 
	ConnectBtnStr.set("Connect") 
	AZStatusStr.set("AZ Status: " + rc.statusAZ)
	ELStatusStr.set("EL Status: " + rc.statusEL)

def buildControlFrame():
	controlFrame = Tkinter.Frame(height=60,bd=1)
	currentRALabel = Tkinter.Label(master=controlFrame,text="Current RA: unknown",padx=100,anchor="w")
	currentRALabel.grid(row=0,column=1,sticky="W")
	currentDecLabel = Tkinter.Label(master=controlFrame,text="Current Dec: unknown",justify=Tkinter.RIGHT,padx=100)
	currentDecLabel.grid(row=0,column=2)
	targetRALabel = Tkinter.Label(master=controlFrame,text="Target RA: none")
	targetRALabel.grid(row=2,column=1)
	targetDecLabel = Tkinter.Label(master=controlFrame,text="Target Dec: none")
	targetDecLabel.grid(row=2,column=2)
	AZStatusLabel = Tkinter.Label(master=controlFrame,textvariable=AZStatusStr)
	AZStatusLabel.grid(row=3,column=1)
	ELStatusLabel = Tkinter.Label(master=controlFrame,textvariable=ELStatusStr)
	ELStatusLabel.grid(row=3,column=2)
	controlFrame.pack(side=Tkinter.BOTTOM)
	connectBtn = Tkinter.Button(master=controlFrame, textvariable=ConnectBtnStr, command=_connect)
	connectBtn.grid(row=4,column=3)
	homeBtn = Tkinter.Button(master=controlFrame, text="HOME", command=_connect)
	homeBtn.grid(row=4,column=1)

def buildSkyPlot():
	fig = Figure(figsize=(5, 4), dpi=100)
	fig.add_subplot(111).plot()
	canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
	canvas.draw()
	canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)
	canvas.get_tk_widget().pack(side=Tkinter.TOP, fill=Tkinter.BOTH, expand=1)


def updateStatus():
	AZStatusStr.set("AZ Status: " + rc.statusAZ)
	ELStatusStr.set("EL Status: " + rc.statusEL)



root = Tkinter.Tk()
root.wm_title("SRT Dish Control")

#Variables for gui details
AZStatusStr = StringVar()
ELStatusStr = StringVar()
ConnectBtnStr = StringVar()


buildGUI()
Tkinter.mainloop()
