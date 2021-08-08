from event_broker import Client, ErrorEvent
from sht30_sensor import Sht30Sensor, SensorReadError
from sht30_sensor_reader.SensorReading import SensorReading

SENSOR_READ_PERIOD_SECONDS = 5 * 60


def main():
    sensor = Sht30Sensor()
    client = Client('sht30SensorReader')
    while True:
        try:
            client.emit_event(SensorReading(sensor.temperature, sensor.humidity))
        except SensorReadError as e:
            client.emit_event(ErrorEvent(str(e)))
        finally:
            client.idle(SENSOR_READ_PERIOD_SECONDS)


if __name__ == '__main__':
    main()
