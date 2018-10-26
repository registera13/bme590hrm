import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy import signal

class ECGProcess
    def __init__(self, file_path, time_units=1, voltage_units=1, window_size=10):
        # validate data and get time/voltage lists

        self.time_units = time_units
        self.voltage_units = voltage_units
        (self.time, self.voltage) = self.parse_data(self.data)
        # determine basic attributes
        self.voltage_extremes = self.get_voltage_extremes()
        self.duration = self.get_duration()
        # first get interval over entire signal
        (self.peak_interval, self.interval_loc) = self.get_peak_interval(self.voltage)
        # then, get the heart rate over pre-specified chunks of time
        self.mean_hr_bpm = self.get_mean_hr(window_size)
        # beat position attributes
        self.peaks = self.locate_peaks()
        self.beats = np.empty(shape=(0, 0))
        if (self.peaks.size > 0):
            self.beats = self.time[self.peaks]
        self.num_beats = self.beats.size
        # export data
        self.export_JSON('{}.json'.format(self.path))
        self.logger.info('HRMonitor object created.')

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


    def bandpass(self,start,stop):
        bp_Hz = np.zeros(0)
        bp_Hz = np.array([start,stop])
        b, a = signal.butter(3, bp_Hz/(self.fs_Hz / 2.0),'bandpass')
        print("Bandpass filtering to: " + str(bp_Hz[0]) + "-" + str(bp_Hz[1]) + " Hz")
        return signal.lfilter(b, a, self.data, 0)