""" Controller.py 
    this package serves as the link between the GUI front end and the hardware motor controller for the radio telescope. 

    Nathan Thomas
    1/17/19
"""
from skyfield.api import Topos, load
import constant
import threading


class Tracking:

	def __init__(self,target,location):
		self.target = target
		self.location = location
		self.ts = load.timescale()


	def setTarget(self, target):
		self.target = target

	def setLocation(self, location):
		self.location = location

	def calcAltAz(self):
		t = self.ts.now()
		apparent = self.location.at(t).observe(self.target).apparent().altaz()
		print apparent[0]
		print apparent[0].degrees	
		return apparent
		
