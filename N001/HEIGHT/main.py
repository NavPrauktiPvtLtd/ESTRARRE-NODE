#!/usr/bin/env python

import time
import json

from N001.HEIGHT.driver.VL53L1X import VL53L1X
import os
import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%d-%m-%Y %H:%M:%S')

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
    try:
        tof = VL53L1X(i2c_bus=1, i2c_address=0x29)
        tof.open()
        # print('open')

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
    # for i in range(1):
    
    # print("Distance: {}cm".format(distance_in_cm))

        count = 0
        status = True
        prev_data = 0
        while status:
            distance_in_cm = (tof.get_distance())/10
            data = round(distance_in_cm,1)
            if abs(prev_data-data) < 1:
                count +=1
            # else:
            #     if(count > 0):
            #         count = 0
            if count == 3:
                status = False
                #return data
            prev_data =data

        return data
    except Exception as e:
        logging.exception(e)

# for i in range(10):
#     data = get_height_data()
#     print(data)
# print(get_height_data())
# hal["SENSOR_CONTROL"]["POWER_OFF"] = 1
# with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/HEIGHT/hal.json", "w") as f:
#     json.dump(hal, f, indent=4)


# f.close()