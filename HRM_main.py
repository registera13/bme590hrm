from ReadData import DataIO
import HRM_SignalProcess as hb

if __name__ == '__main__':
    Inputdata= DataIO("test_data1.csv")
    Inputdata.read_data()
    Inputdata.extract_data()
    hb.process(Inputdata.volt, 0.75, 333)
    # We have imported our Python module as an object called 'hb'
    # This object contains the dictionary 'measures' with all values in it
    # Now we can also retrieve the BPM value (and later other values) like this:
    bpm = hb.measures['bpm']
    # To view all objects in the dictionary, use "keys()" like so:
    print
    hb.measures.keys()




