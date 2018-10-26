import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
from scipy import signal

class ECG
    def __init__(self, time, voltage, hrw, fs):
        # validate data and get time/voltage lists

        self.time= time
        self.voltage=voltage
        self.hrw = hrw
        self.fs = fs

    def rolmean(self, dataset=self.voltage, hrw=self.hrw, fs=self.fs):
        mov_avg = dataset['hart'].rolling(int(hrw * fs)).mean()
        avg_hr = (np.mean(dataset.hart))
        mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
        mov_avg = [x * 1.2 for x in mov_avg]
        dataset['hart_rollingmean'] = mov_avg


    def find_peaks(self):
        """Locates the S wave peak in the signal
            1st) filter signal using a a bandpass filter

        :return: array with approximate locations of beats given as indices of the time array
        """


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


    def bandpass(self,start,stop):
        bp_Hz = np.zeros(0)
        bp_Hz = np.array([start,stop])
        b, a = signal.butter(3, bp_Hz/(self.fs_Hz / 2.0),'bandpass')
        print("Bandpass filtering to: " + str(bp_Hz[0]) + "-" + str(bp_Hz[1]) + " Hz")
        return signal.lfilter(b, a, self.data, 0)