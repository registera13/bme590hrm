from ReadData import DataIO
from SignalProcess import ECG


def main(filename):
    # read and export data to array
    inputdata = DataIO(filename)
    inputdata.read_data()
    # import data into signal process
    dataset = ECG(inputdata.time, inputdata.voltage)
    num_beats, beats = dataset.count_beats()
    voltage_extremes = dataset.get_voltage_extremes()
    time_duration = dataset.get_duration()
    avg_hr_bpm = dataset.mean_heart_rate()

    ecg_outputs = {"Mean Heart Rate BPM": avg_hr_bpm,
                   "Minimum Voltage": voltage_extremes[0],
                   "Maximum Voltage": voltage_extremes[1],
                   "Duration": time_duration,
                   "Number of Beats": num_beats,
                   "Beats": str(beats)}
    dataset.write_json(ecg_outputs, inputdata.filename)

    print(inputdata.ospath)
    print(inputdata.filename)


if __name__ == '__main__':
    main("test_data13.csv")




