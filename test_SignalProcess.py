from ReadData import DataIO
from SignalProcess import ECG
import pytest
from pytest import approx


@pytest.mark.parametrize("filename,expected", [
    ('test_data1.csv', 27.775),
    ('test_data3.csv', 27.775),
    ('test_data12.csv', 13.887),
    ('test_data28.csv', 27.775),
])
def test_get_duration(filename, expected):
    """
    test_get_duration checked those listed files manually for duration
    """
    inputdata = DataIO(filename)
    inputdata.read_data()
    # import data into signal process
    dataset = ECG(inputdata.time, inputdata.voltage)
    assert dataset.get_duration() == expected


@pytest.mark.parametrize("filename,expected", [
    ('test_data1.csv', (-0.68, 1.05)),
    ('test_data12.csv', (-0.523, 0.584)),
])
def test_get_voltage_extremes(filename, expected):
    """
    test_get_voltage_extremes checked those listed files manually for voltage in excel
    used rel .001 to compare expected
    """

    inputdata = DataIO(filename)
    inputdata.read_data()
    # import data into signal process
    dataset = ECG(inputdata.time, inputdata.voltage)
    assert approx(dataset.get_voltage_extremes(), rel=1e-2) == expected

@pytest.mark.parametrize("filename,expected", [
    ('test_data1.csv', 35),
    ('test_data2.csv', 33),
])
def test_count_beats(filename,expected):
    inputdata = DataIO(filename)
    inputdata.read_data()
    # import data into signal process
    dataset = ECG(inputdata.time, inputdata.voltage)
    num_beats, beats = dataset.count_beats()
    assert num_beats == expected

