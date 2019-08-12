"""
    Test driver for the controllers
"""
import threading, time
from skyfield.api import Topos, load, Star
from controller import RotorController
from tracking import Tracking

def __start():
	print "boom"
	listener = threading.Thread(target=track, args=())                                            
	e = threading.Event()                                                                                        
	listener.start() 


def track(): 
	while True:
		#check if rotor is moving
		print "checking movement"
		print Rotor.isMoving()
		if Rotor.isMoving():
			print "Rotor moving, sleeping"
			time.sleep(1)
		else: 
			print "Rotor stopped, calculating"

			print Tracker.calcAltAz()

	

#setup location
planets = load('de421.bsp')
earth = planets['earth']

location = earth + Topos('36.31205 N', '81.35347 W')


#setup test target
#barnard = Star(ra_hours=(17,57,48.49803), dec_degrees(4,41,36.2072))
barnard = Star(ra_hours=(16, 51, 47.29), dec_degrees=(-22, 6, 26.3))
Tracker = Tracking(barnard,location)

Tracker.calcAltAz()


Rotor = RotorController()
Rotor.connect("/dev/ttyACM0")
Rotor.move(.5,1)
__start()


