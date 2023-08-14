from typing import Union
from fastapi import FastAPI, HTTPException
import logging
#from N001.TEMPERATURE.main import get_temp_data
from N001.TEMPERATURE.i2c_to_pi import get_temp_data
from N001.HEIGHT.main import get_height_data
from N001.WEIGHT.main import get_weight_data
from N001.WEIGHT.calib import offset_calc, ratio_calc, set_calib_value
import psutil
import speedtest
import json

app = FastAPI()

speed_test = speedtest.Speedtest(secure=True)

def bytes_to_mb(bytes):
  KB = 1024 # One Kilobyte is 1024 bytes
  MB = KB * 1024 # One MB is 1024 KB
  return int(bytes/MB)

# Logging file initialisation
logging.basicConfig(filename="event.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Sensor dictionary
sensor = {'2':"HEIGHT",
          '5':"TEMPERATURE",
          '6':'WEIGHT'}

@app.get("/")
async def read_root():
    
    # Logging the GET request
    logging.info("GET /")
    
    data = await set_calib_value()
    
    # Logging the data
    logging.info(data)
    return data 


# Data request from sensors
@app.get("/sensor/{sensor_id}/start")
async def read_item(sensor_id: str, q: Union[str, None] = None):
    
    # logging the GET request
    logging.info("GET /sensor/" + sensor_id + "/start")
    try:
        if sensor_id == '2':
            data = await get_height_data()
        if sensor_id == '5':
            data = get_temp_data()
        if sensor_id == '6':
            data = get_weight_data()
            
        logging.info(data)

        return {"sensor_id": sensor_id,"sensor_name":sensor[sensor_id], 'data': data}
    except:
        
        # Logging the error
        logging.error("Invalid Sensor ID")
        
        return {"error": "Invalid Sensor ID"}


# Calibration of sensors
@app.get("/sensor/weight/calib/{step}")
async def read_item(step: str,offset: Union[int, None] = None, ratio: Union[float, None] = None):
    
    # Logging the GET request
    logging.info("GET /sensor/weight/calib/" + step)
    
    try:
        if step == '1':
            data = await offset_calc()
            return {"data_type":'offset', 'data': data}
        if step == '2':
            data = await ratio_calc()
            return {"data_type":'ratio', 'data': data}
        if step == '3':
            set_calib_value(offset, ratio)
            return {"success": "data_recieved"}
    
    except Exception as e:
        
        # Logging the error
        logging.error(e)
        return {"error": "invalid step", "data": str(e)}
    
@app.get("/system/health")
async def system_health():
    logging.info("GET /system/health")
    try:
        download_speed = bytes_to_mb(speed_test.download())
        print("Your Download speed is", download_speed, "MB")
        upload_speed = bytes_to_mb(speed_test.upload())
        print("Your Upload speed is", upload_speed, "MB")

        health = {
            "ram": {
                "percentage used": psutil.virtual_memory()[2],
                "total(GB)": psutil.virtual_memory()[1]/1000000000,
                "used(GB)": psutil.virtual_memory()[3]/1000000000
            },
            #"temp": psutil.sensors_temperatures(fahrenheit=False)[2],
            "storage": {
                "total(GB)": psutil.disk_usage('/')[0]/1000000000,
                "used(GB)": psutil.disk_usage('/')[1]/1000000000
            },
            "cpu(%)": psutil.cpu_percent(4),
            "network_speed(MB)": {
                "download": download_speed,
                "upload": upload_speed
            }
        }
        #print(health)
        return {"health": health, "success": True}
    
    except Exception as e:
        print(e)
        return {"error": "Something went wrong", "success": False}
        
@app.get("/sensor/health")
async def sensor_health():
    logging.info("GET /sensor/health")
    faulty_sensors = []
    try:
        temp = get_temp_data()
        if(temp == None):
            faulty_sensors.append("Temperature")
        
        height = await get_height_data()
        if(height == None):
            faulty_sensors.append("Height")
            
        weight = get_weight_data()
        if(weight == None):
            faulty_sensors.append("Weight")
        
        
        
        return {"faulty_sensors" : faulty_sensors}
    except Exception as e:
        print(e)
        return {"error": "Something went wrong", "success": False}
        