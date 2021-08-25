#!/bin/bash

trap 'kill %1; kill %2' SIGINT
python water_valve_controller/main.py &
python humidity_monitor/main.py &
python sht30_sensor_reader/main.py
