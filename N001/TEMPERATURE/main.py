#!/usr/bin/env python3
import serial
import time

import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%d-%m-%Y %H:%M:%S')

def get_temp_data():
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        ser.reset_input_buffer()

        ser.write(b"a\n")
        line = ser.readline().decode('utf-8').rstrip()
        #print(line)
        time.sleep(1)
        return line
    except Exception as e:
        logging.error(e)