from datetime import datetime, timedelta

from event_broker import EventHandler, Client, Error
from humidity_monitor import LowHumidity
from water_valve import WaterValve, WaterValveError
from water_valve_controller import WaterValveOpened

MIN_TIME_BETWEEN_OPENING_WATER_VALVE = timedelta(minutes=10)
WATER_VALVE_OPEN_TIME_SECONDS = 6

water_valve = WaterValve()
last_opened_time = datetime(2011, 1, 1).astimezone()


def low_humidity_detected(client: Client, _):
    global water_valve, last_opened_time
    now = datetime.now().astimezone()
    if now - last_opened_time > MIN_TIME_BETWEEN_OPENING_WATER_VALVE:
        try:
            water_valve.open(WATER_VALVE_OPEN_TIME_SECONDS)
            last_opened_time = now
            client.emit_event(WaterValveOpened(WATER_VALVE_OPEN_TIME_SECONDS))
        except WaterValveError as e:
            client.emit_event(Error(str(e)))


def main():
    low_humidity_detected_handler = EventHandler(LowHumidity, low_humidity_detected)
    client = Client('WaterValveController', [low_humidity_detected_handler], ignore_missed_messages=True)
    client.listen()


if __name__ == '__main__':
    main()
