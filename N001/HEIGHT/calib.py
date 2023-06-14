# • For fast and high-accuracy long ranging (>2000 mm):
#      – Total air gap and cover window thickness = 1 mm maximum
#      – Cover window thickness <0.6 mm and air gap <0.4 mm
#      – Gasket and/or light blocker enhances performance (see Section 5.2.7 Use of a gasket)
# • For sub 1000 mm ranging:
#      – Total air gap and cover window thickness = 2 mm maximum
#      – Cover window thickness <1.5 mm and air gap <0.5 mm
#      – Gasket is required

import time
import logging
import driver.VL53L1X as VL53L1X
logging.basicConfig(filename="error.log",level=logging.DEBUG, format='%(asctime)s-%(levelname)s- %(message)s',
                     datefmt='%Y-%m-%d %H:%M:%S')

try:

    tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
    tof.open()

    tof.start_ranging(1)  # Start ranging
                        # 0 = Unchanged
                        # 1 = Short Range(upto 1.3 meter)
                        # 2 = Medium Range(upto 3 meter)
                        # 3 = Long Range(upto 4 meter)



    dis_known=0#input("Enter the distance in cm", )
    data = []

    # for i in range(50):
    distance_in_cm = (tof.get_distance())/10 
    data.append(distance_in_cm)
    print("Distance: {}cm".format(distance_in_cm))
    time.sleep(1)
    dis_measured= sum(data)/len(data)
    calib = int(dis_known) - dis_measured
    print(calib)
except Exception as e:
    logging.error('critical')
