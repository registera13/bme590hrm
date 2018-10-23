
def voltage_maxmin(ecg_data):

    volt_data = ecg_data[:, 1]
    max_volt = max(volt_data)
    min_volt = min(volt_data)
    voltage_extremes = (min_volt, max_volt)
    return voltage_extremes