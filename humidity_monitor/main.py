from event_broker import Client, EventHandler
from humidity_monitor.HumidityAlarm import HumidityAlarm
from humidity_monitor.LowHumidity import LowHumidity
from sht30_sensor_reader import HumidityChanged

MIN_HUMIDITY_PERCENT = 70
HUMIDITY_ALARM_PERCENT = 65
WATER_TIME_SECONDS = 6


def humidity_change_received(client: Client, humidity_change: HumidityChanged):
    if humidity_change.humidity < MIN_HUMIDITY_PERCENT:
        client.emit_event(LowHumidity())
    if humidity_change.humidity < HUMIDITY_ALARM_PERCENT:
        client.emit_event(HumidityAlarm(humidity_change.humidity))


def main():
    humidity_change_handler = EventHandler(HumidityChanged, humidity_change_received)
    client = Client('HumidityMonitor', [humidity_change_handler], ignore_missed_messages=True)
    client.listen()


if __name__ == '__main__':
    main()
