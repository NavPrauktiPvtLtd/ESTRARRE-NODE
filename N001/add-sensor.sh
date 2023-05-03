#!/bin/bash

# Ask user for sensor name
echo "Enter sensor name: "
read sensor_name

# Create directory with sensor name in capital letters
mkdir "${sensor_name^^}"

# Create driver directory inside sensor directory
mkdir "${sensor_name^^}"/driver

# Create calib.json, calib.py, hal.json, main.py, and self-test.py files inside sensor directory
touch "${sensor_name^^}"/calib.json
touch "${sensor_name^^}"/calib.py
touch "${sensor_name^^}"/hal.json
touch "${sensor_name^^}"/main.py
touch "${sensor_name^^}"/self-test.py

# Populate hal.json with specified values
hal_json='{
     "SENSOR_CONTROL": {
          "SENSOR-ID": "",
          "CATEGORY": "",
          "NAME": "'"${sensor_name^^}"'",
          "UNIT": "",
          "HW_SERIAL_NUMBER":"" ,
          "HW_PART_NUMBER": "",
          "HW_MANUFACTURER": "",
          "HW_REVISION": "",
          "POWER_OFF": 1,
          "RESET": 0,
          "PLAY": 1,
          "READ_DATA": 1,
          "DATA_TYPE": "INT",
          "WRITE_MEMORY": 0,
          "WRITE_CALIB": 0,
          "READ_MEMORY": 0,
          "READ_CALIB": 0,
          "CALIB_VOID": 1,
          "RUN_SELF_TEST": 0,
          "ERROR_CODE": 0
     },
     "ACTUATOR_CONTROL": {
          "SENSOR-ID": "",
          "CATEGORY":"" ,
          "NAME": "",
          "UNIT": "",
          "HW_SERIAL_NUMBER":"" ,
          "HW_PART_NUMBER": "",
          "HW_MANUFACTURER": "",
          "HW_REVISION":"" ,
          "POWER-OFF": "",
          "RESET": "",
          "RUN": "",
          "WRITE_DATA": "",
          "DATA_TYPE": "",
          "WRITE_MEMORY": "",
          "WRITE_CALIB": "",
          "READ_MEMORY": "",
          "READ_CALIB":"" ,
          "RUN_SELF_TEST": "",
          "ERROR_CODE": ""
     },
     "COMMAND/DATA_TRANSLATION": {
          "CMD_TRANSLATION": 1,
          "DATA_TRANSLATION": 1
     }
}'

echo "${hal_json}" > "${sensor_name^^}"/hal.json