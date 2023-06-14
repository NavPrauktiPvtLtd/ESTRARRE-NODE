import RPi.GPIO as GPIO  # import GPIO
from N001.WEIGHT.driver.hx711 import HX711  # import the class HX711

"""
load cell to Hx711
white- A-
Green- A+
Red- Supply +
Black- Supply -


Hx711 to raspberry pi
GND- GND pin 39
DT- GPIO 21
SCK- GPIO 20
Vcc- pin 2
"""
import json
# import os
# cwd = os.getcwd()
# path = cwd + "/hal."
with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/WEIGHT/calib.json", "r") as f:
    calib = json.load(f)


offset = calib["CALIB_VALUE_OFFSET"]
ratio  = calib["CALIB_VALUE_RATIO"]
f.close()


import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%d-%m-%Y %H:%M:%S')


# try:
#     GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
#     # Create an object hx which represents your real hx711 chip
#     # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
#     hx = HX711(dout_pin=21, pd_sck_pin=20)
#     hx.set_offset(offset)
#     hx.set_scale_ratio(ratio)
#     print("Now, I will read data in infinite loop. To exit press 'CTRL + C'")
#     input('Press Enter to begin reading')
#     print('Current weight on the scale in grams is: ')
#     while True:
#         print(round(((hx.get_weight_mean(20))/1000),1), 'kg')

# except (KeyboardInterrupt, SystemExit):
#     print('Bye :)')

# finally:
#     GPIO.cleanup()

def get_weight_data():
    try:
        #GPIO intialisation
        GPIO.setmode(GPIO.BCM)
        # HX711 class declaration
        hx = HX711(dout_pin=21, pd_sck_pin=20)
        #Setting offset and 
        hx.set_offset(offset)
        hx.set_scale_ratio(ratio)
        data = round(((hx.get_weight_mean(20))/1000),1)
        # print(data, 'kg')

        count = 0
        status = True
        prev_data = 0
        while status:
            data = round(((hx.get_weight_mean(20))/1000),1)
            if abs(prev_data-data) < 0.3:
                count +=1
            else:
                if(count > 0):
                    count = 0
            if count == 3:
                status = False
                #return data
            prev_data =data

        if data < 1:
            return 0
        else:
            return data
        
    except Exception as e:
        logging.error(e)
        

