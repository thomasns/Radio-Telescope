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
		self.statusAZ = constant.MotionStatus[4]
		self.statusEL = constant.MotionStatus[4]
		self.targetAZ = 999; #undefined
		self.targetEL = 999; #undefined	
		self.ser = serial.Serial()

	def connect(self,port):
		""" 
		Open serial connection between program and rotor hardware


		Parameters: 
		port (string): The path/name of the serial port
		"""
		self.ser = serial.Serial(port,timeout=5)
		self.statusAZ = constant.MotionStatus[3]
		self.statusEL = constant.MotionStatus[3]
		line = self.ser.readline() + self.ser.readline() + self.ser.readline()
		self.listener = threading.Thread(target=self.__checkFeedback, args=())
		self.e = threading.Event()
		self.listener.start()
		return line

	def disconnect(self):
		"""Closes the serial connection."""
		
		self.ser.close()
		self.statusAZ = constant.MotionStatus[4]
		self.statusEL = constant.MotionStatus[4]

	def moveHome(self):
	    	"""Move the rotor to it's home location"""
		
		if self.statusAZ == constant.MotionStatus[4] or self.statusEL == constant.MotionStatus[4]:
			raise Exception('Not connected to motor controller')

		#send command to move here
		self.statusAZ = constant.MotionStatus[2]
		self.statusEL = constant.MotionStatus[2]
		
		#lock until home

		self.statusAZ = constant.MotionStatus[0]
		self.statusEL = constant.MotionStatus[0]
		self.currentAZ = constant.AZ_HOME
		self.currentEL = constant.EL_HOME 


	def move(self,targetAlt,targetAz):
		""" 
		Move the rotor to the specificed Altitude and Azmith

		Tells the rotor hardware how many ticks to move each axis and begins monintoring controller feedback. 

		Parameters: 
		targetAlt (float): The altitude the rotor should slew to, must be between 0 and 90. 
		targetAz (float): The azmith the rotor should slew to, must be between 0 and 360. 
		"""
		#sanity checks
		if self.statusAZ == constant.MotionStatus[4]:
			raise Exception('Not connected to motor controller')
                if targetAlt < 0 or targetAlt > 90:
                    raise Exception('targetAlt should be between 0 and 90. targetAlt was: {}'.format(targetAlt))
                if targetAz < 0 or targetAz > 360:
                    raise Exception('targetAz should be between 0 and 360. targetAz was: {}'.format(targetAz))

		#set up EL motion
		steps = int((targetAlt - self.currentEL) / self.EL_DEGREES_PER_TICK)
		if(steps < 0):
			dir = 'p'
		else:
			dir = 'n'
		#send EL  move commend
		self.__sendCommand('move EL ' + dir +  ' ' + str(steps/1))
		#set up AZ motion
		steps = int((targetAz - self.currentAZ) / self.AZ_DEGREES_PER_TICK)
		if(steps < 0):
			dir = 'p'
		else:
			dir = 'n'
		self.__sendCommand('move AZ ' + dir +  ' ' + str(steps/1))
		self.statusAZ = constant.MotionStatus[1]
		self.statusEL = constant.MotionStatus[1]
		self.e.set()

	def isMoving(self):
		""" 
		Checks to see if the rotor is moving

		Partial implementation. Need to update after moving from rotor simulator to hardware

		Returns:True if either axis is moving, otherwise false
		"""
		if self.statusAZ == constant.MotionStatus[0] and self.statusEL == constant.MotionStatus[0]:
			return False
		return True

        #parses a command from the rotorController
	def __parseFeedback(self, line):
		""" 
		Parses a line of feedback from the controller

		Parses feedback from the rotor controller, and updates status in the class
		
		Paramaters:
		line (String): the line of feedback from the rotor controller hardware
		"""

		command = line.split(':')[0]
		params = line.split(':')[1]

		if command == 'STEPPED':
			if params == 'AZ':
			    self.currentAZ += self.AZ_DEGREES_PER_TICK
			elif params == 'EL':
			    self.currentEL += self.AZ_DEGREES_PER_TICK
			print("\033[1;34m" + 'Moved 1 pules on the ' + params + ' axis' + "\033[0;0m")
			#do something
		elif command == 'STOPPED':
			print( 'Finished travel on the ' + params + ' axis')
			print params
			if params.strip() == 'AZ':
				self.statusAZ = constant.MotionStatus[0]
			elif params.strip() == 'EL':
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
			print("\033[1;31m" + 'Reveived a ' + params.split(' ')[0] + ' warning on the ' + params.split(' ')[1] + ' axis' + "\033[0;0m")
			#do something:

	def __sendCommand(self,command):
		""" 
		Sends a command to the rotor controller.

		Sends a command to the rotor controller. Do not use directly, let this class handle it
		
		Paramaters:
		line (String): the command to send
		"""
		if self.statusAZ == constant.MotionStatus[4]:
			raise Exception('Not connected to motor controller')
		if self.ser.is_open:
			print 'Sending command: ' + command
			self.ser.write(command + "\n")
				
		else:
			raise Exception('Serial port not open')

	#this should be opened as a thread once the port has been opened
	def __checkFeedback(self):
		""" 
		Checks to see if the rotor controller has a line of feedback in the buffer

		Checks to see if any feedback is avilable. If any is, read it and begin parsing. 
		This method should be ran as a thread when a command has been sent to the controller
		
		"""
		while True:
			self.e.wait()
			while self.ser.in_waiting > 0:
				line = self.ser.readline()
				if line[0] != ':': #i've set the controller to echo commmands back for debugging, prepended with a ':'. This ignores those lines
					self.__parseFeedback(line)
				else:
					print "\033[1;31m" + ' ' + line + "\033[0;0m"

