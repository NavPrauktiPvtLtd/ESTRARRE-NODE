import numpy as np
import driver.MAX30102 as MAX30102
import matplotlib.pyplot as plt
from hr_fft import inverse_fft
# 25 samples per second (in algorithm.h)
SAMPLE_FREQ = 25
# taking moving average of 4 samples when calculating HR
# in algorithm.h, "DONOT CHANGE" comment is attached
MA_SIZE = 4
# sampling frequency * 4 (in algorithm.h)
BUFFER_SIZE = 100



# this assumes ir_data and red_data as np.array
def calc_spo2(ir_data, red_data):

    # red_mean = int(np.mean(red_data))
    # x = -1 * (np.array(red_data) - red_mean)
    # x1=[]
    # for i in range(x.shape[0]-MA_SIZE):
    #     x1.append((np.sum(x[i:i+MA_SIZE]) / MA_SIZE))
    # calculate threshold
    # n_th = int(np.mean(x))
    # n_th = 30 if n_th < 30 else n_th  # min allowed
    # n_th = 60 if n_th > 60 else n_th  # max allowed 
    y_filtered= inverse_fft(red_data, BUFFER_SIZE)
    fig, ax = plt.subplots(1, 1)
    ax.plot(range(100),y_filtered[:100])
    plt.show()

    ir_valley_locs, n_peaks = find_peaks(y_filtered[:100], BUFFER_SIZE, 4)
    print(ir_valley_locs)

    # ---------spo2---------

    # find precise min near ir_valley_locs (???)
    exact_ir_valley_locs_count = n_peaks

    # find ir-red DC and ir-red AC for SPO2 calibration ratio
    # find AC/DC maximum of raw

    # FIXME: needed??
    for i in range(exact_ir_valley_locs_count):
        if ir_valley_locs[i] > BUFFER_SIZE:
            spo2 = -999  # do not use SPO2 since valley loc is out of range
            spo2_valid = False
            return spo2, spo2_valid

    i_ratio_count = 0
    ratio = []

    # find max between two valley locations
    # and use ratio between AC component of Ir and Red DC component of Ir and Red for SpO2
    red_dc_max_index = -1
    ir_dc_max_index = -1
    for k in range(exact_ir_valley_locs_count-1):
        red_dc_max = -16777216
        ir_dc_max = -16777216
        if ir_valley_locs[k+1] - ir_valley_locs[k] > 3:
            # print("ir vally location"+ str(ir_valley_locs[k])+" "+str(ir_valley_locs[k+1]))
            for i in range(ir_valley_locs[k], ir_valley_locs[k+1]):
                if ir_data[i] > ir_dc_max:
                    ir_dc_max = ir_data[i]
                    ir_dc_max_index = i
                if red_data[i] > red_dc_max:
                    red_dc_max = red_data[i]
                    red_dc_max_index = i
            # print("ir dc max:"+str(ir_dc_max)+" in location-"+str(ir_dc_max_index))
            # print("red dc max:"+str(red_dc_max)+" in location-"+str(red_dc_max_index))

            red_ac = int((red_data[ir_valley_locs[k+1]] - red_data[ir_valley_locs[k]]) * (red_dc_max_index - ir_valley_locs[k]))
            red_ac = red_data[ir_valley_locs[k]] + int(red_ac / (ir_valley_locs[k+1] - ir_valley_locs[k]))
            red_ac = red_data[red_dc_max_index] - red_ac  # subtract linear DC components from raw

            ir_ac = int((ir_data[ir_valley_locs[k+1]] - ir_data[ir_valley_locs[k]]) * (ir_dc_max_index - ir_valley_locs[k]))
            ir_ac = ir_data[ir_valley_locs[k]] + int(ir_ac / (ir_valley_locs[k+1] - ir_valley_locs[k]))
            ir_ac = ir_data[ir_dc_max_index] - ir_ac  # subtract linear DC components from raw

            nume = red_ac * ir_dc_max
            denom = ir_ac * red_dc_max
            if (denom > 0 and i_ratio_count < 5) and nume != 0:
                # original cpp implementation uses overflow intentionally.
                # but at 64-bit OS, Pyhthon 3.X uses 64-bit int and nume*100/denom does not trigger overflow
                # so using bit operation ( &0xffffffff ) is needed
                ratio.append(int(((nume * 100) & 0xffffffff) / denom))
                i_ratio_count += 1

    # choose median value since PPG signal may vary from beat to beat
    ratio = sorted(ratio)  # sort to ascending order
    print(ratio)
    mid_index = int(i_ratio_count / 2)

    ratio_ave = ratio[0]
    # if mid_index > 1:
    #     ratio_ave = int((ratio[mid_index-1] + ratio[mid_index])/2)
    # else:
    #     if len(ratio) != 0:
    #         ratio_ave = ratio[mid_index]

    # # why 184?
    print("ratio average: ", ratio_ave)
    if ratio_ave > 2 and ratio_ave < 184:
        # -45.060 * ratioAverage * ratioAverage / 10000 + 30.354 * ratioAverage / 100 + 94.845
        # a, b, c values taken from here- https://github.com/vrano714/max30102-tutorial-raspberrypi/blob/master/hrcalc.py
        
        spo2 = -45.060 * (ratio_ave**2) / 10000.0 + 30.054 * ratio_ave / 100.0 + 94.845

        # spo22= 104 - 17 * (ratio_ave/100)
        # spo23= 110 - 25 * (ratio_ave/100)
        spo2_valid = True
    else:
        spo2 = -999
        spo2_valid = False

    return spo2, spo2_valid


def find_peaks(x, size,min_dist):
    """
    Find at most MAX_NUM peaks above MIN_HEIGHT separated by at least MIN_DISTANCE
    """
    ir_valley_locs, n_peaks = find_peaks_above_min_height(x, size)
    ir_valley_locs, n_peaks = remove_close_peaks(n_peaks, ir_valley_locs, x, min_dist)

    # n_peaks = min([n_peaks, max_num])

    return ir_valley_locs, n_peaks


def find_peaks_above_min_height(x, size):
    """
    Find all peaks above MIN_HEIGHT
    """

    i = 0
    n_peaks = 0
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
                ir_valley_locs.append(i)
                n_peaks += 1  # original uses post increment
                i += n_width + 1
            else:
                i += n_width
        else:
            i += 1

    return ir_valley_locs, n_peaks


def remove_close_peaks(n_peaks, ir_valley_locs, x, min_dist):
    """
    Remove peaks separated by less than MIN_DISTANCE
    """

    # should be equal to maxim_sort_indices_descend
    # order peaks from large to small
    # should ignore index:0
    sorted_indices = sorted(ir_valley_locs, key=lambda i: x[i])
    sorted_indices.reverse()

    # this "for" loop expression does not check finish condition
    # for i in range(-1, n_peaks):
    i = -1
    while i < n_peaks:
        old_n_peaks = n_peaks
        n_peaks = i + 1
        # this "for" loop expression does not check finish condition
        # for j in (i + 1, old_n_peaks):
        j = i + 1
        while j < old_n_peaks:
            n_dist = (sorted_indices[j] - sorted_indices[i]) if i != -1 else (sorted_indices[j] + 1)  # lag-zero peak of autocorr is at index -1
            if n_dist > min_dist or n_dist < -1 * min_dist:
                sorted_indices[n_peaks] = sorted_indices[j]
                n_peaks += 1  # original uses post increment
            j += 1
        i += 1

    sorted_indices[:n_peaks] = sorted(sorted_indices[:n_peaks])

    return sorted_indices, n_peaks 

def rem_of_base_var(data):
    data[0:2] = np.mean(data)
    signal = np.array(data)
    mean = np.mean(signal)
    std = np.std(signal)
    normalized_signal = (signal - mean)/std
    return normalized_signal


# Generate a sample signal
t = range(BUFFER_SIZE)

for i in range(10): 
    m = MAX30102.MAX30102()
    red_data, ir_data, _= m.read_sequential(BUFFER_SIZE)
    red_data = np.array(red_data)
    ir_data = np.array(ir_data)
# red_data = rem_of_base_var(red_data)
# ir_data = rem_of_base_var(ir_data)
    spo2, valid_spo2 = calc_spo2(ir_data, red_data)
    if spo2 > 80:
        print(round(spo2,), valid_spo2)
    # fig, (ax1, ax2) = plt.subplots(2, 1)
    # ax1.plot(t, red_data)
    # ax1.set_xlabel('Time')
    # ax1.set_ylabel('RED DATA')
    # ax2.plot(t,ir_data )
    # ax2.set_xlabel('Time')
    # ax2.set_ylabel('IR DATA')
    # plt.show()
    fig, ax = plt.subplots()
    ax.plot(t, red_data, label='RED')
    ax.plot(t, ir_data, label='IR')

    ax.legend()
    plt.show()
# plotting


m.shutdown()