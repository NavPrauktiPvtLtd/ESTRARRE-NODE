#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from N001.WEIGHT.driver.hx711 import HX711  # import the class HX711

import json

# path = cwd + "/hal."

import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%d-%m-%Y %H:%M:%S')



async def offset_calc():
        GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
        # Create an object hx which represents your real hx711 chip
        # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
        hx = HX711(dout_pin=21, pd_sck_pin=20)
        # measure tare and save the value as offset for current channel
        # and gain selected. That means channel A and gain 128
        err = hx.zero()

        # check if successful
        if err:
            # raise ValueError('Tare is unsuccessful.')
            logging.error('Tare is unsuccessful.')
        reading = hx.get_raw_data_mean()
       
        # if reading:  # always check if you get correct value or only False
        #     # now the value is close to 0
        #     print('Data subtracted by offset but still not converted to units:',
        #         reading)
        # else:
        #     print('invalid data', reading)
        return reading
async def ratio_calc():
        GPIO.setmode(GPIO.BCM) 
        hx = HX711(dout_pin=21, pd_sck_pin=20)
        # In order to calculate the conversion ratio to some units, in my case I want grams,
        # you must have known weight.
        # input('Put known weight on the scale and then press Enter')
        reading = hx.get_data_mean()
        # if reading:
        #     print('Mean value from HX711 subtracted by offset:', reading)
        #     known_weight_grams = input(
        #         'Write how many grams it was and press Enter: ')
        #     try:
        #         value = float(known_weight_grams)
        #         print(value, 'grams')
        #     except ValueError:
        #         print('Expected integer or float and I have got:',
        #             known_weight_grams)
        value = 64300 # kept golden weight of 10kg

            # set scale ratio for particular channel and gain which is
            # used to calculate the conversion to units. Required argument is only
            # scale ratio. Without argumen    calib["CALIB_VALUE_OFFSET"] = errts 'channel' and 'gain_A' it sets
            # the ratio for current channel and gain.
        ratio = reading / value  # calculate the ratio for channel A and gain 128
         # set ratio for current channel
        # print('Ratio is set.')
        # else:    # measure tare and save the value as offset for current channel
        # # and gain selected. That means channel A and gain 128
        
    
        # # Read data several times and return mean value
        # # subtracted by offset and converted by scale ratio to
        # # desired units. In my case in grams.
        #     raise ValueError('Cannot calculate mean value. Try debug mode. Variable reading:', reading)

        # Read data several times and return mean value
        # subtracted by offset and converted by scale ratio to
        # desired units. In my case in grams.
        GPIO.cleanup()
        return ratio

    # except (KeyboardInterrupt, SystemExit):
    #     print('Bye :)')

    # finally:
        # GPIO.cleanup()
def set_calib_value(offset, ratio):
    with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/WEIGHT/calib.json", "r") as f:
        calib = json.load(f)

    calib["CALIB_VALUE_OFFSET"] = offset
    calib["CALIB_VALUE_RATIO"] = ratio 
    with open("/home/pi/PROJECTS/ESTRARRE-NODE/N001/WEIGHT/calib.json", "w") as f:
        json.dump(calib, f, indent=4)
    f.close()  
    return 
