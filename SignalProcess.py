import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.mlab as mlab
from scipy import signal
import math


class ECG
    def __init__(self, time, voltage, minvoltage =None, maxvoltage = None):
        # validate data and get time/voltage lists

        self.timearray= time
        self.voltagearray=voltage
        self.hrw = hrw
        self.fs = fs

    def autocorr(self):
        """
        Compute the autocorrelation of the voltage, based on the properties of the
        power spectral density of the signal.
        from: https://stackoverflow.com/questions/643699/how-can-i-use-numpy-correlate-to-do-autocorrelation
        :return: Autocorrelated dataset
        """
        x = self.voltagearray
        result = (numpy.correlate(x, x, mode='full'))
        result = result[len(result) // 2:]
        logger.info('Autocorrelation Successful')
        return result

    def get_interval(self):
        """
        Using autocorr() to find the length of the peak to peak R-wave interval
        See https://www.mathworks.com/help/signal/ug/find-periodicity-using-autocorrelation.html
        for detail
        :return: time in seconds of the R to R peak
        """
        data = self.autocorrelate()
        data = data ** 2
        peaks_indices = scipy.signal.find_peaks_cwt(data, numpy.arange(5, 10),min_snr=2)
        # create array to store the indices
        max_values = []
        for n, i in enumerate(peaks_indices):
            max_values.append(data[i])
        interval_time_index = peaks_indices[1]
        interval = self.timevals[interval_time_index]
        logger.info('get autocorr interval successful')
        return interval
    def count_beats(self):
        interval_sec = self.get_interval()
        interval_indices = self.timearray.index(interval_sec)
        num_intervals = int(max(self.timearray) / interval_sec)

        # Create interval "search bins" in which to find local peaks
        bin_ends = []
        for i in range(1, num_intervals + 1):
            bin_ends.append((i * interval_indices) - 1)
        bin_ends.append(len(self.voltagearray))
        start = 0
        peak_val = []
        peak_val_index = []

        for n, i in enumerate(bin_ends):
            bin = self.voltagearray[start:i]
            peak_val.append(max(bin))
            peak_val_location = start + bin.index(peak_val[n])
            peak_val_index.append(peak_val_location)
            start = i + 1

        peak_val_times = []
        for i in peak_val_index:
            peak_val_times.append(self.timearray[i])

        # Collect Desired Values
        num_beats = len(peak_val)
        beats = numpy.array(peak_val_times)
        self.num_beats = num_beats
        self.beat_times = beats
        return num_beats, beats

def find_peaks(self, dataset):
        """Locates the S wave peak in the signal
            1st) filter signal using a a bandpass filter

        :return: array with approximate locations of beats given as indices of the time array
        """
        window = []
        peaklist = []
        listpos = 0
        for datapoint in dataset.hart:
            rollingmean = dataset.hart_rollingmean[listpos]
            if (datapoint < rollingmean) and (len(window) < 1):
                listpos += 1
            elif (datapoint > rollingmean):
                window.append(datapoint)
                listpos += 1
            else:
                maximum = max(window)
                beatposition = listpos - len(window) + (window.index(max(window)))
                peaklist.append(beatposition)
                window = []
                listpos += 1
        measures['peaklist'] = peaklist
        measures['ybeat'] = [dataset.hart[x] for x in peaklist]

        return peaks

    def get_peak_interval(self, data):
        """Determines interval between peaks using auto-correlation

        :param data: data interval to process into heart
        :return: tuple containing (interval size between ECG peaks in seconds, array index of interval location)
        """
        self.logger.info('Calculating interval between peaks...')
        # calculate autocorrelation and square the data
        raw_corrl = np.correlate(data, data, mode='full')
        correl = raw_corrl[raw_corrl.size // 2:]
        sq_cor = np.square(correl)

        # find position after first peak (DC)
        after_peak = 0
        prev = sq_cor[0]
        for i in range(sq_cor.size):
            if (sq_cor[i] <= prev):
                after_peak = i
                prev = sq_cor[i]
            else:
                break

        # find position of 2nd peak to get interval between peaks
        interval_loc = after_peak + np.argmax(sq_cor[after_peak:], axis=0)
        interval_val = self.time[interval_loc]
        self.logger.info('Interval between peaks is {}.'.format(interval_val))
        return (interval_val, interval_loc)

    def get_mean_hr(self, window_size):
        """Determines heart rate (bpm) for block chunks

        :param window_size: size of window to determine heart rate for
        :return: numpy vector of heart rate for each block interval
        """

        self.logger.info('Calculating mean heart rate...')
        heart_rates = []
        prev_index = 0
        prev_time = self.time[prev_index]
        for i, time in enumerate(self.time):
            if (time >= window_size + prev_time or i == len(self.time) - 1):
                (int_val, int_loc) = self.get_peak_interval(
                    self.voltage[prev_index:i])

                heart_rate = (60 / int_val).round(5)
                heart_rates.append(heart_rate)

                prev_index = i
                prev_time = time

        self.logger.info(
            'Heart rates determined for {} blocks'.format(len(heart_rates)))
        return np.asarray(heart_rates)

    def get_duration(self):
        """Calculates the duration of the ECG signal

        :return: difference between the first and last time value
        """
        duration = self.time[-1] - self.time[0]
        return duration

    def get_voltage_extremes(self):
        """
        Calculate the Max and Min of the input voltage
        :return: (min,max) vaulues
        """
        extremes = (min(self.voltage), max(self.voltage))
        return extremes



    def export_JSON(self, file_path):
        """Exports calculated attributes to a json file

        :param file_path: json file path to export to
        """
        # first, create a dict with the attributes
        dict_with_data = {
            'peak_interval': round(self.peak_interval, 3),
            'mean_hr_bpm': self.mean_hr_bpm.tolist(),
            'voltage_extremes': self.voltage_extremes,
            'duration': self.duration,
            'num_beats': self.num_beats,
            'beats': self.beats.tolist(),
        }

        # convert dict to json, and write it to file
        self.logger.info('Saving data to JSON file...')
        json_with_data = json.dumps(dict_with_data, sort_keys=False)
        with open(file_path, 'w') as f:
            f.write(json_with_data)

        self.logger.info('Data saved to {}.'.format(file_path))
