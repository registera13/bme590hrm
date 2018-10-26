from ReadData import DataIO
from SignalProcess import ECG

def main(filename):
    # read and export data to array
    Inputdata = DataIO(filename)
    Inputdata.read_data()
    # import data into signal process
    dataset = ECG(Inputdata.time,Inputdata.voltage)
    num_beats, beats = dataset.count_beats()
    voltage_extremes = dataset.get_voltage_extremes()
    time_duration = dataset.get_duration()
    avg_hr_bpm = dataset.get_mean_hr_bpm()

    ECG_outputs = {"Mean Heart Rate BPM": avg_hr_bpm,
                   "Minimum Voltage (%s)": voltage_extremes[0],
                   "Maximum Voltage (%s)": voltage_extremes[1],
                   "Duration of Reading": time_duration,
                   "Number of Beats": num_beats,
                   "Beat Times": str(beats)}
    dataset.write_json(ECG_outputs)

if __name__ == '__main__':
    main(filename)




