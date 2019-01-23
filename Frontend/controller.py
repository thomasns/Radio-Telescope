""" Controller.py 
    this package serves as the link between the GUI front end and the hardware motor controller for the radio telescope. 

    Nathan Thomas
    1/17/19
"""
import constant
import threading
import serial


class RotorController:

	def __init__(self):
		self.AZ_DEGREES_PER_TICK = 1/constant.AZ_TICKS_PER_DEGREE
		self.EL_DEGREES_PER_TICK = 1/constant.EL_TICKS_PER_DEGREE
		self.directionAZ = 0 # undefined direction
		self.directionEL = 0 # undefined direction
		self.currentAZ = 0 # undefined Azmith
		self.currentEL = 0 # undefined Elevation
		self.statusAZ = constant.MotionStatus[3]
		self.statusEL = constant.MotionStatus[3]
		self.targetAZ = 999; #undefined
		self.targetEL = 999; #undefined	
		self.ser = serial.Serial('/dev/ttyACM0',timeout=5)
		line = self.ser.readline() + self.ser.readline() + self.ser.readline();

		self.listener = threading.Thread(target=self.checkFeedback, args=())
		self.e = threading.Event()
		self.listener.start()
		print line

	def moveHome(self):
		#send command to move here
		self.statusAZ = constant.MotionStatus[2]
		self.statusEL = constant.MotionStatus[2]
		
		#lock until home

		self.statusAZ = constant.MotionStatus[0]
		self.statusEL = constant.MotionStatus[0]
		self.currentAZ = constant.AZ_HOME
		self.currentEL = constant.EL_HOME 


	def move(self,RA,DEC):
	
		#sanity checks
                if(RA < -90 or RA > 90):
                    raise Exception('RA should be between -90 and 90. RA was: {}'.format(RA))
                if(DEC < -180 or DEC > 180):
                    raise Exception('DEC should be between -180 and 180. DEC was: {}'.format(DEC))

		#set up EL motion
		steps = int((RA - self.currentEL) / self.EL_DEGREES_PER_TICK)
		if(steps < 0):
			dir = 'p'
		else:
			dir = 'n'
		#send EL  move commend
		self.sendCommand('move EL ' + dir +  ' ' + str(steps/1))
		#set up AZ motion
		steps = int((DEC - self.currentAZ) / self.AZ_DEGREES_PER_TICK)
		if(steps < 0):
			dir = 'p'
		else:
			dir = 'n'
		self.sendCommand('move AZ ' + dir +  ' ' + str(steps/1))
		self.statusAZ = constant.MotionStatus[1]
		self.statusEL = constant.MotionStatus[1]
		while self.ser.out_waiting > 0:
			pass
		self.e.set()

        #parses a command from the rotorController
	def parseFeedback(self, line):
		command = line.split(':')[0]
		params = line.split(':')[1]

		if command == 'STEPPED':
			if params == 'AZ':
			    self.currentAZ += self.AZ_DEGREES_PER_TICK
			elif params == 'EL':
			    self.currentEL += self.AZ_DEGREES_PER_TICK
			print('Moved 1 pules on the ' + params + ' axis')
			#do something
		elif command == 'STOP':
			print( 'Finished travel on the ' + params + ' axis')
			if params == 'AZ':
				self.statusAZ = constant.MotionStatus[0]
			elif params == 'EL':
				self.statusEL = constant.MotionStatus[0]
			if self.statusAZ == constant.MotionStatus[0] and self.statusEL == constant.MotionStatus[0]:
				self.e.clear()
	
			
                #do something
		elif command == 'HOME':
			print('Arrived home on the ' + params + ' axis')
			self.currentAZ = 0
			self.currentEl = 0
			#do something
		elif command == 'WARN':
			print('Reveived a ' + params.split(' ')[0] + ' warning on the ' + params.split(' ')[1] + ' axis')
			#do something:

	def sendCommand(self,command):
		print 'Sending command: ' + command
		if self.ser.is_open:
			self.ser.write(command)
		else:
			raise Exception('Serial port not open')

	#this should be opened as a thread once the port has been opened
	def checkFeedback(self):
		while True:
			self.e.wait()
			while self.ser.in_waiting > 0:
				line = self.ser.readline()
				self.parseFeedback(line)


