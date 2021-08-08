#!/bin/bash

docker create -it -p 1883:1883 -v "$(pwd)"/mosquitto.conf:/mosquitto/config/mosquitto.conf --name mqtt_server eclipse-mosquitto:2.0.11
