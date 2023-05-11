#!/usr/bin/env python

import time
import json

from .driver.VL53L1X import VL53L1X
import os



# cwd = os.getcwd()
# path = cwd + "/hal."
# with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/HEIGHT/hal.json", "r") as f:
#     hal = json.load(f)
# # POWER_OFF is low while running this script
# hal["SENSOR_CONTROL"]["POWER_OFF"] = 0
# with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/HEIGHT/hal.json", "w") as f:
#     json.dump(hal, f, indent=4)



# Open and start the VL53L1X sensor.
# If you've previously used change-address.py then you
# should use the new i2c address here.
# If you're using a software i2c bus (ie: HyperPixel4) then
# you should `ls /dev/i2c-*` and use the relevant bus number.
async def get_height_data():
    tof = VL53L1X(i2c_bus=1, i2c_address=0x29)
    tof.open()
    print('open')

    # Optionally set an explicit timing budget
    # These values are measurement time in microseconds,
    # and inter-measurement time in milliseconds.
    # If you uncomment the line below to set a budget you
    # should use `tof.start_ranging(0)`
    # tof.set_timing(66000, 70)

    tof.start_ranging(1)  # Start ranging
                        # 0 = Unchanged
                        # 1 = Short Range
                        # 2 = Medium Range
                        # 3 = Long Range
    # while running:
    print('ranging')
    distance = []
    # for i in range(1):
    distance_in_mm = tof.get_distance()
    print("Distance: {}mm".format(distance_in_mm))
    time.sleep(0.1)
    distance.append(distance_in_mm)
    # distance = []

    return distance_in_mm


# print(get_height_data())
# hal["SENSOR_CONTROL"]["POWER_OFF"] = 1
# with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/HEIGHT/hal.json", "w") as f:
#     json.dump(hal, f, indent=4)


# f.close()