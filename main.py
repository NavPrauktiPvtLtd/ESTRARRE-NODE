from typing import Union
from fastapi import FastAPI, HTTPException
import logging
from N001.TEMPERATURE.main import get_temp_data
from N001.HEIGHT.main import get_height_data
from N001.WEIGHT.main import get_weight_data
from N001.WEIGHT.calib import offset_calc, ratio_calc, set_calib_value

app = FastAPI()

# Logging file initialisation
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S')

# Sensor dictionary
sensor = {'2':"HEIGHT",
          '5':"TEMPERATURE",
          '6':'WEIGHT'}

@app.get("/")
async def read_root():
    data = await set_calib_value()
    return data 


# Data request from sensors
@app.get("/sensor/{sensor_id}/start")
async def read_item(sensor_id: str, q: Union[str, None] = None):
    try:
        if sensor_id == '2':
            data = await get_height_data()
        if sensor_id == '5':
            data = get_temp_data()
        if sensor_id == '6':
            data = get_weight_data()

        return {"sensor_id": sensor_id,"sensor_name":sensor[sensor_id], 'data': data}
    except:
        return 'Invalid Sensor ID'


# Calibration of sensors
@app.get("/sensor/weight/calib/{step}")
async def read_item(step: str,offset: Union[int, None] = None, ratio: Union[float, None] = None,):
    try:
        if step == '1':
            data = await offset_calc()
            return {"data_type":'offset', 'data': data}
        if step == '2':
            data = await ratio_calc()
            return {"data_type":'ratio', 'data': data}
        if step == '3':
            set_calib_value(offset, ratio)
            return 'data_recieved'
    except Exception as e:
        return 'invalid step'
    