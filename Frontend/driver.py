"""
    Test driver for the controllers
"""

from controller import RotorController


rc = RotorController()
print rc.AZ_DEGREES_PER_TICK
print rc.statusAZ
print rc.statusEL
rc.moveHome()
print rc.statusAZ
print rc.statusEL

rc.move(90,30)
print rc.statusAZ
print rc.statusEL

rc.parseCommand('HOME:EL')
print rc.currentAZ
rc.parseCommand('STEP:AZ')
print rc.currentAZ
rc.parseCommand('WARN:THERMAL AZ')

