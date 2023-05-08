# • For fast and high-accuracy long ranging (>2000 mm):
#      – Total air gap and cover window thickness = 1 mm maximum
#      – Cover window thickness <0.6 mm and air gap <0.4 mm
#      – Gasket and/or light blocker enhances performance (see Section 5.2.7 Use of a gasket)
# • For sub 1000 mm ranging:
#      – Total air gap and cover window thickness = 2 mm maximum
#      – Cover window thickness <1.5 mm and air gap <0.5 mm
#      – Gasket is required

import time

import HEIGHT.driver.VL53L1X as VL53L1X

tof = VL53L1X.VL53L1X(i2c_bus=1, i2c_address=0x29)
tof.open()

tof.start_ranging(1)  # Start ranging
                      # 0 = Unchanged
                      # 1 = Short Range
                      # 2 = Medium Range
                      # 3 = Long Range



dis_known=input("Enter the distance", )
data = []
for i in range(5):
    distance_in_mm = tof.get_distance()
    data.append(distance_in_mm)
    # print("Distance: {}mm".format(distance_in_mm))
    time.sleep(0.5)
dis_measured= sum(data)/len(data)
calib = dis_known - dis_measured
print(calib)