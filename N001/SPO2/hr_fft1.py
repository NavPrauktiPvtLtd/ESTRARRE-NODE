import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


import json
import driver.MAX30102 as MAX30102

def rem_of_base_var(data):
    data[0:2] = np.mean(data)
    signal = np.array(data)
    mean = np.mean(signal)
    std = np.std(signal)
    normalized_signal = (signal - mean)/std
    return normalized_signal


def find_peaks(x, y,  size):
    
    #Find all peaks 
    
    

    i = 0
    max_value = 0
    max_freq = 0
    ir_valley_locs = []  # [0 for i in range(max_num)]
    while i < size - 1:
        if x[i] > x[i-1]:  # find the left edge of potential peaks
            n_width = 1
            # original condition i+n_width < size may cause IndexError
            # so I changed the condition to i+n_width < size - 1
            while i + n_width < size - 1 and x[i] == x[i+n_width]:  # find flat peaks
                n_width += 1
            if x[i] > x[i+n_width]:  # find the right edge of peaks
                # ir_valley_locs[n_peaks] = i
                ir_valley_locs.append(x[i])
                if x[i] > max_value:
                    max_value = x[i]
                    max_freq = y[i]
                i += n_width + 1
            else:
                i += n_width
        else:
            i += 1

    return ir_valley_locs, max_value, max_freq
sample_size = 100
# Generate a sample signal
t = range(sample_size)

m = MAX30102.MAX30102()

for i in range(5):

    red_data, _, _= m.read_sequential(sample_size)
    red_data = np.array(red_data)
    
    red_data = rem_of_base_var(red_data)
# Compute the FFT of the signal
    fft_result = np.fft.fft(red_data,1000)

# Compute the frequency axis. d= 1/f 
    freq_axis = np.fft.fftfreq(1000, d=0.04)
    """
    # Filter out frequencies above 4 Hz
fft_y_filtered = fft_result.copy()
fft_y_filtered[np.abs(freq_axis) > 2 ] = 0
fft_y_filtered[np.abs(freq_axis) < 0.5 ] =0
# Compute the inverse FFT to get the filtered signal
y_filtered = np.fft.ifft(fft_y_filtered)
"""
#find the peak frequency

    Power_fft= np.abs(fft_result)**2
    _, max_mag, max_freq = find_peaks(Power_fft[20:120], freq_axis[20:120], 100) 

# Plot the signal and its FFT


    # fig, (ax1, ax2) = plt.subplots(2, 1)
    # ax1.plot(t, red_data)
    # ax1.set_xlabel('Time')
    # ax1.set_ylabel('Amplitude')
    # ax2.plot(freq_axis,Power_fft )
    # ax2.set_xlabel('Frequency')
    # ax2.set_ylabel('Magnitude')
    # plt.show()  

    print(round(max_freq*60, ))

m.shutdown()