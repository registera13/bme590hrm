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
try:
    import logging
except ImportError:
    print('Could not import logging')

class DataIO:

    def __init__(self, filename):
        self.filename = filename
        self.ospath = os.getcwd()
        self.folderpath = "test_data"
        self.fullfolderpath = os.path.join(self.ospath, self.folderpath, filename)

        self.cvsName = filename
        self.csvDf = None

        logging.basicConfig(filename="DataIO_log.txt",
                            format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')
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

        headers = ['Time', 'Voltage']
        df = pd.read_csv(self.fullfolderpath, names=headers)
        self.csvDf = df

    def extract_data(self):
        tempVolt = pd.to_numeric(self.csvDf.Voltage, errors='coerce')
        tempTime = pd.to_numeric(self.csvDf.Time, errors='coerce')

        self.volt = pd.DataFrame(tempVolt).interpolate().values.ravel().tolist()
        self.times = pd.DataFrame(tempTime).interpolate().values.ravel().tolist()

        #plt.title("CVS Heart Rate Signal")
        #plt.plot(tempTime,tempVolt)
        #plt.show()


if __name__ == '__main__':
    Inputdata= DataIO("test_data1.csv")
    Inputdata.read_data()
    Inputdata.extract_data()



