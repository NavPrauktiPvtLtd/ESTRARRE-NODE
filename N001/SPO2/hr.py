import numpy as np
import matplotlib.pyplot as plt

import json
import driver.MAX30102 as MAX30102


"""
Pin Config
Vcc- 5v
SDA- GPIO 2
SCL- GPIO 3
GND- GND
"""

sample_size = 200
# Generate a sample signal
t = range(sample_size)
# moving average size
MA_SIZE=20 

m = MAX30102.MAX30102()

#for reading data via the sensor
red_data, _, _= m.read_sequential(sample_size)
red_data = np.array(red_data)

#storing the data in a file
file= open("red_data.txt", "w")
file.write(str(red_data))
file.close()

mean_y2 = []

#moving average 
for i in range(red_data.shape[0]-MA_SIZE):
    # if i in range(MA_SIZE):
    #     mean_y2.append(ecg_y1[i])
    # else:
    mean_y2.append(1.00049*(np.sum(red_data[i:i+MA_SIZE]) / MA_SIZE))
    #1.00049 is used to lift the moving avg graph over the red_data array so that low amplitude peaks can be omitted for calculation


def find_peaks(y, x,moving_avg, ma_size):
    
    #Find all peaks 
    
    size = y.shape[0]-MA_SIZE

    i = 0
    max_value = 0

    peak_loc = []  # [0 for i in range(max_num)]
    while i < size - 1:
        if y[i] > y[i-1]:  # find the left edge of potential peaks
            n_width = 1
            # original condition i+n_width < size may cause IndexError
            # so I changed the condition to i+n_width < size - 1
            while i + n_width < size - 1 and y[i] == y[i+n_width]:  # find flat peaks
                n_width += 1
            if y[i] > y[i+n_width]:  # find the right edge of peaks
                # ir_valley_locs[n_peaks] = i
                
                # if the value of an element in red_data array is greater than that of the moving_avg 
                # array, then we append the location in the peak_loc array 
                if y[i] > moving_avg[i]:
                    peak_loc.append(x[i])
                  
                i += n_width + 1
            else:
                i += n_width
        else:
            i += 1

    return peak_loc

peaks= find_peaks(red_data, t, mean_y2, MA_SIZE)
difference= np.diff(peaks) # difference of elements in the array
mean_diff= np.mean((difference)*0.04) #1/f= 0.04
frequency= 1/mean_diff
hr_value= frequency*60
print(hr_value)
# print((1/(np.mean(np.diff(peaks))*0.04))*60)  This prints the HR value as well 
fig, ax = plt.subplots()
ax.plot(t, red_data, label='Data 1')
ax.plot(t[:red_data.shape[0]-MA_SIZE], mean_y2, label='Data 2')

ax.legend()
m.shutdown()
plt.show()