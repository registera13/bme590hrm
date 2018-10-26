import pytest
import numpy

def test_ReadData():
    """
    Test input datafile 4 first and last time and voltage is correct
    :return:
    """
    from ReadData import DataIO
    testObj1 = DataIO('test_data4.csv')
    testObj1.read_data()
    assert testObj1.time[0] == 0
    assert testObj1.voltage[0] == -0.375
    assert testObj1.time[-1] == 27.775
    assert testObj1.voltage[-1] == -0.365



