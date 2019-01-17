from enum import Enum

AZ_TICKS_PER_DEGREE = 11.7
EL_TICKS_PER_DEGREE = 11.7

AZ_HOME = 0
EL_HOME = 0

STATION_LAT = 36.381355 
STATION_LON = -82.4155
STATION_ALT = 453

MotionStatus = ['Stopped', 'Moving', 'Homing', 'Stopped/Unverified']

CONTROLLER_PORT = '/dev/ttyACM0'
