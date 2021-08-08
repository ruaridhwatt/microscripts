from config import is_raspberrypi

if is_raspberrypi():
    from sht30_sensor.Sht30Sensor import Sht30Sensor
else:
    from sht30_sensor.MockSht30Sensor import MockSht30Sensor as Sht30Sensor

from sht30_sensor.SensorReadError import SensorReadError
