"""
    Test driver for the controllers
"""
import threading, time
from skyfield.api import Topos, load, Star
from controller import RotorController
from tracking import Tracking

def __start():
	listener = threading.Thread(target=track, args=())                                            
	e = threading.Event()                                                                                        
	listener.start() 


def track(): 
	while True:
		#check if rotor is moving
		print Rotor.isMoving()
		if Rotor.isMoving():
			print "Rotor moving, sleeping"
			time.sleep(5)
		else: 
			print "Rotor stopped, calculating"

			alt,az, dist =  Tracker.calcAltAz()
			Rotor.move(alt.degrees,az.degrees)
	

#setup location
planets = load('de421.bsp')
earth = planets['earth']

location = earth + Topos('36.31205 N', '81.35347 W')


#setup test target
#barnard = Star(ra_hours=(17,57,48.49803), dec_degrees(4,41,36.2072))
testTarget = Star(ra_hours=(22, 57, 39.52), dec_degrees=(-29,37,24))
Tracker = Tracking(testTarget,location)

Tracker.calcAltAz()


Rotor = RotorController()
Rotor.connect("/dev/ttyACM0")
Rotor.move(0,0)
__start()


