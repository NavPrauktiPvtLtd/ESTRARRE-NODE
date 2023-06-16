from smbus2 import SMBus
from time import sleep
import logging

import logging
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%d-%m-%Y %H:%M:%S')

class MLX90614():
    #ambiant temperature
    MLX90614_TA = 0x06
    # Object 1 temperature
    MLX90614_TOBJ1 = 0x07

    

    comm_retries = 5
    comm_sleep_amount = 0.1

    def __init__(self, bus, address=0x5A):
        self.bus = bus
        self.address = address

    def read_reg(self, reg_addr):
        err = None
        for i in range(self.comm_retries):
            try:
                return self.bus.read_word_data(self.address, reg_addr)
            except IOError as e:
                err = e
                # "Rate limiting" - sleeping to prevent problems with sensor
                # when requesting data too quickly
                sleep(self.comm_sleep_amount)
        # By this time, we made a couple requests and the sensor didn't respond
        # (judging by the fact we haven't returned from this function yet)
        # So let's just re-raise the last IOError we got
        raise err

    def read_temp(self, reg):
        data = self.read_reg(reg)
        temp = (data * 0.02) - 273.15
        return temp

    def get_amb_temp(self):
        return self.read_temp(self.MLX90614_TA)

    def get_obj_temp(self):
        return self.read_temp(self.MLX90614_TOBJ1)



def get_temp_data():
    try:
        channel = 1
        bus = SMBus(channel)
        sensor = MLX90614(bus, address=0x5A)
        amb_temp=round(sensor.get_amb_temp(), 2)
        obj_temp=round(sensor.get_obj_temp(), 2)
    # print ('Ambiant temperature: '+ str(amb_temp)+'˚C')
    
    # print ('Object temperature: '+ str(obj_temp)+'˚C')
        bus.close()
        return obj_temp
    except Exception as e:
        logging.error(e)