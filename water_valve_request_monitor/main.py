from datetime import datetime, timedelta

from event_broker import EventHandler, Client, ErrorEvent
from humidity_monitor import OpenWaterValveRequest
from water_valve import WaterValve, WaterValveError
from water_valve_request_monitor import WaterValveOpenedEvent, OpenWaterValveRequestDenied

MIN_TIME_BETWEEN_OPENING_WATER_VALVE = timedelta(minutes=5)

water_valve = WaterValve()
last_opened_time = datetime(2011, 1, 1).astimezone()


def open_water_valve_request_received(client: Client, request: OpenWaterValveRequest):
    global water_valve, last_opened_time
    now = datetime.now().astimezone()
    if now - last_opened_time > MIN_TIME_BETWEEN_OPENING_WATER_VALVE:
        try:
            water_valve.open(request.time_seconds)
            last_opened_time = now
            client.emit_event(WaterValveOpenedEvent(request.time_seconds))
        except WaterValveError as e:
            client.emit_event(ErrorEvent(str(e)))
    else:
        client.emit_event(OpenWaterValveRequestDenied('Too soon'))


def main():
    open_water_valve_request_handler = EventHandler(OpenWaterValveRequest, open_water_valve_request_received)
    client = Client('WaterValveRequestMonitor', [open_water_valve_request_handler], ignore_missed_messages=True)
    client.listen()


if __name__ == '__main__':
    main()
