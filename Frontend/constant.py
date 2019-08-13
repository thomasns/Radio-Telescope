from enum import Enum

#AZ_TICKS_PER_DEGREE = 11.7
#ALT_TICKS_PER_DEGREE = 11.7
AZ_TICKS_PER_DEGREE = 3.0 #must be entered as a floating point number (add a .0 to the end if value is round)
ALT_TICKS_PER_DEGREE = 3.0 #must be entered as a floating point number

AZ_HOME = 0
EL_HOME = 0

STATION_LAT = 36.381355 
STATION_LON = -82.4155
STATION_ALT = 453

MotionStatus = ['Stopped', 'Moving', 'Homing', 'Stopped/Unverified','Disconnected']

CONTROLLER_PORT = '/dev/ttyACM0'
