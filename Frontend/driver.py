"""
    Test driver for the controllers
"""

from controller import RotorController


rc = RotorController()
print rc.AZ_DEGREES_PER_TICK

rc.move(90,30)



