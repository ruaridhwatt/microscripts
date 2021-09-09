## Getting Started
To get started, clone the kompetensdag branch of the microscripts repo:
```
git clone -b kompetensdag https://github.com/ruaridhwatt/microscripts.git
```
Create a new virtual environment in the microscripts project directory:
```
python3 -m venv microscripts/venv
```
Activate the virtual environment:
```
source microscripts/venv/bin/activate
```
Install the requirements:
```
pip install -r microscripts/requirements.txt
```
Install the project modules:
```
pip install -e microscripts
```
Open the project in your favourite Python IDE (PyCharm).

## Setting up the code templates (Pycharm specific)

Now you can copy the file templates to the .idea directory for use in Pycharm:
```
cd microscripts
cp -r fileTemplates .idea
```
Update PyCharm to use the project code templates:

Pycharm>Preferences...  
Editor>File and Code Templates  
Scheme: Project

## Start the Docker MQTT Broker
There are a few helper scripts in `docker_mqtt_server`.
Create and start the MQTT message broker:
```
cd docker_mqtt_server
./create_mqtt_server.sh
./start_mqtt_server.sh
```

## Part 1
Create a new python package, `sensor_reader`, which will publish humidity changes to MQTT.

In the newly created package, create a new Event using the Event template with filename `HumidityChange` and field name `humidity`.

Create a new `main.py` file in `sensor_reader` which
1. Creates a Sht30Sensor instance
2. Creates a Client instance with QOS 0
3. Uses the client to publish a HumidityChange event every 10 seconds

The following imports may help you get started:
```
from sht30_sensor import Sht30Sensor
from event_broker import Client, QualityOfService
from sensor_reader.HumidityChange import HumidityChange
```

Try running the sensor reader and check the `microscripts.log` file to see what is being published.

## Part 2
Create a new service, `humidity_monitor`. This service's client will subscribe to the HumidityChange events with QOS 0 and choose to start with a clean session (`ignore_missed_messages=True`).

In the `EventHandler` callback, print the humidity received.

Stop and start the humidity monitor to verify that the message broker does not queue missed messages.

### Retained Flag
Set the retained flag for messages published by `sensor_reader`.
Verify that an initial, retained message is immediately available to the `humidity_monitor` upon subscription.

### Persistent session
Remove the retained flag from `sensor_reader` and clear the retained message from the topic.
Update `humidity_monitor` so that it initiates a persistent session (`ignore_missed_messages=False`).

Verify that messages are **not** queued due to the QOS of the subsription being 0.

Update the QOS of `humidity_monitor` subscription to 1.
Verify that messages are now queued for the `humidity_monitor`.


