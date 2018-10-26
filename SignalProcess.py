try:
    import pandas as pd
except ImportError:
    print('Could not import pandas')
try:
    import matplotlib.pyplot as plt
except ImportError:
    print('Could not import matplot')
try:
    import numpy
except ImportError:
    print('Could not import numpy')
try:
    import logging
except ImportError:
    print('Could not import logging')

import scipy.signal
import logging

log_format = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='divlog.txt', format=log_format,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,
                    filemode='w')
logger = logging.getLogger()


class ECG:
    def __init__(self, time, voltage, minvoltage=None, maxvoltage=None,
                num_beats=None, beat_times=None,
                duration=None, mean_hr=None):
        # validate data and get time/voltage lists

        self.timearray = time
        self.voltagearray = voltage
        self.minvoltage = minvoltage
        self.maxvoltage = maxvoltage
        self.num_beats = num_beats
        self.beat_times = beat_times
        self.duration = duration
        self.mean_hr = mean_hr

    def get_duration(self):
        """Calculates the duration of the ECG signal

        :return: difference between the first and last time value
        """
        duration = self.timearray[-1] - self.timearray[0]
        self.duration = duration
        return duration

    def get_voltage_extremes(self):
        """
        Calculate the Max and Min of the input voltage
        :return: (min,max) values
        """
        self.minvoltage = min(self.voltagearray)
        self.maxvoltage = max(self.voltagearray)
        extremes = (min(self.voltagearray), max(self.voltagearray))
        return extremes

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
        data = self.autocorr()
        data = data ** 2
        peaks_indices = scipy.signal.find_peaks_cwt(data, numpy.arange(5, 10), min_snr=2)
        # create array to store the indices
        max_values = []
        for n, i in enumerate(peaks_indices):
            max_values.append(data[i])
        interval_time_index = peaks_indices[1]
        interval = self.timearray[interval_time_index]
        logger.info('get autocorr interval successful')
        return interval

    def count_beats(self):
        """
        Find the Number of beats using the given interval calculated from get_interval()
        method used from http://greenteapress.com/thinkdsp/html/thinkdsp006.html
        and https://stackoverflow.com/questions/3684484/peak-detection-in-a-2d-array
        :return: times when the beats occurred
        """
        interval_sec = self.get_interval()
        interval_indices = self.timearray.index(interval_sec)
        num_intervals = int(max(self.timearray) / interval_sec)

        bin_ends = []
        for i in range(1, num_intervals + 1):
            bin_ends.append((i * interval_indices) - 1)
        bin_ends.append(len(self.voltagearray))
        start = 0
        peak_val = []
        peak_val_index = []

        for n, i in enumerate(bin_ends):
            bins = self.voltagearray[start:i]
            peak_val.append(max(bins))
            peak_val_location = start + bins.index(peak_val[n])
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

    def mean_heart_rate(self):
        """ Calculates heart rate of the sample data in BPM
        :returns: avg_hr_bpm: calculated heart rate in beats per minute
        """
        avg_bps = self.num_beats / self.duration
        # convert sec to min
        avg_bpm = int(avg_bps * 60)
        self.mean_hr = avg_bpm
        return avg_bpm

    def write_json(self, dictionary, path = None , filename = 'data1'):
        """ Writes data outputs to json files using
            https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
        :param: dictionary: dictionary containing the data to be written
                to a json file
                path: path to the file to be written
                filename: name of the file in string, should be the input filename
        :returns: json file with the same name as the input file"""

        import json
        with open(path + filename + '.json', 'w') as outfile:
            json.dump(dictionary, outfile)
        logger.info('Calculated data written to %s' % filename + '.json')

