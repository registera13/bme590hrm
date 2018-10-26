import os
try:
    import pandas as pd
except ImportError:
    print('Could not import pandas')
try:
    import matplotlib.pyplot as plt
except ImportError:
    print('Could not import matplot')
try:
    import numpy as np
except ImportError:
    print('Could not import numpy')
import csv

import logging
log_format = '%(levelname)s %(asctime)s %(message)s'
logging.basicConfig(filename='LOG_DataIO.txt', format=log_format,
                    datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG,
                    filemode='w')
logging = logging.getLogger()


class DataIO:

    def __init__(self, filename):
        self.filename = filename
        self.ospath = os.getcwd()
        self.folderpath = "test_data"
        self.fullfolderpath = os.path.join(self.ospath, self.folderpath, filename)

        self.cvsName = filename
        self.csvDf = None

        if not self:
            logging.warning('filename is empty')
            raise ValueError("filename is empty")
        if not isinstance(filename, str):
            logging.warning('file name is not in string format')
            raise TypeError("file name is not in string format")
        if ".csv" not in filename:
            logging.warning('file is not a .csv file')
            raise TypeError("file is not a .csv file")

    def read_data(self):
        try:
            self.fullfolderpath + 'test'
        except TypeError:
            print('Input file name must be a String type')
            logging.warning('Input file entered was not a String type')
            raise TypeError('Input file entered was not a String type')
            return None
        try:
            pd.read_csv(self.fullfolderpath)
        except FileNotFoundError:
            print('No file with given filename found')
            logging.debug('No file with given filename found')
            raise FileNotFoundError('No file with given filename found')
            return None

        with open(self.fullfolderpath, 'r') as my_data:
            csv_reader = csv.reader(my_data, delimiter=',')
            time = []
            voltage = []
            for n, reading in enumerate(csv_reader):
                time.append(float(reading[0]))
                voltage.append(float(reading[1]))
            self.time = time
            self.voltage =voltage
            logging.info('Reading of %s' % self.filename + 'was successful from %s' + self.fullfolderpath)


        #plt.title("CVS Heart Rate Signal")
        #plt.plot(tempTime,tempVolt)
        #plt.show()


if __name__ == '__main__':
    Inputdata= DataIO("test_data1.csv")
    Inputdata.read_data()
    #print(Inputdata.time)
    #print(Inputdata.voltage)




