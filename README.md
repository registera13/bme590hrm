# bme590hrm
BME 590 Heart Rate Monitor

[![Build Status](https://travis-ci.com/registera13/bme590hrm.svg?branch=master)](https://travis-ci.com/registera13/bme590hrm)

#introduction
This is a project for BME 590 Medical Device Development class. The goal of this project is to analyze an ECG signal in a .cvs file and
compute mean heart rate BPM, maximum and  minimum voltage, duration of ECG, number of beats, and the time when a beat takes place. 


# Program Overview
This program contain 3 important files ReadData.py, SignalPorcess.py, and HRM_main which is a scripted program that calls 
the function in the other 2 files


# Instruction for use the program
1) all .csv files should be in test_data folder for the program to call them
2) install requirement.txt packages
3) run HRM_main.py may need to modifiy the filename in the .py files. In next version will add a user input option
4)  json files will be stored under the same path as the HRM_main.py file with the save inputed filename

