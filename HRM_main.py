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
    avg_hr_bpm = dataset.mean_hr_bpm()

    ecg_outputs = {"Mean Heart Rate BPM": avg_hr_bpm,
                   "Minimum Voltage (%s)": voltage_extremes[0],
                   "Maximum Voltage (%s)": voltage_extremes[1],
                   "Duration of Reading": time_duration,
                   "Number of Beats": num_beats,
                   "Beat Times": str(beats)}
    dataset.write_json(ecg_outputs, inputdata.ospath, inputdata.filename)

if __name__ == '__main__':
    main(filename)




