from event_broker import Client, EventHandler
from humidity_monitor import OpenWaterValveRequest
from sht30_sensor_reader import SensorReading

MIN_HUMIDITY = 70
WATER_TIME_SECONDS = 10


def sensor_reading_received(client: Client, sensor_reading: SensorReading):
    if sensor_reading.humidity < MIN_HUMIDITY:
        client.emit_event(OpenWaterValveRequest(WATER_TIME_SECONDS))


def main():
    sensor_reading_handler = EventHandler(SensorReading, sensor_reading_received)
    client = Client('HumidityMonitor', [sensor_reading_handler], ignore_missed_messages=True)
    client.listen()


if __name__ == '__main__':
    main()
