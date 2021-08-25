from event_broker import Client, Error
from sht30_sensor import Sht30Sensor, SensorReadError
from sht30_sensor_reader.HumidityChanged import HumidityChanged
from sht30_sensor_reader.TemperatureChanged import TemperatureChanged

SENSOR_READ_PERIOD_SECONDS = 10
TEMPERATURE_RESOLUTION_CELSIUS = 0.1
HUMIDITY_RESOLUTION_PERCENT = 1


def main():
    sensor = Sht30Sensor()
    current_temperature = 0
    current_humidity = 0
    client = Client('sht30SensorReader')
    while True:
        try:
            temperature_reading = sensor.temperature
            humidity_reading = sensor.humidity
            if abs(current_temperature - temperature_reading) > TEMPERATURE_RESOLUTION_CELSIUS:
                client.emit_event(TemperatureChanged(sensor.temperature))
            if abs(current_humidity - humidity_reading) > HUMIDITY_RESOLUTION_PERCENT:
                client.emit_event(HumidityChanged(humidity_reading))
        except SensorReadError as e:
            client.emit_event(Error(str(e)))
        finally:
            client.idle(SENSOR_READ_PERIOD_SECONDS)


if __name__ == '__main__':
    main()
