"""
    Test driver for the controllers
"""

from controller import RotorController

rc = RotorController()
rc.connect("/dev/ttyACM0")
rc.move(5,10)


