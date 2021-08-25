import datetime
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from event_broker import Client, Event, EventHandler, Error
from humidity_monitor import LowHumidity, HumidityAlarm
from sht30_sensor_reader import TemperatureChanged, HumidityChanged
from water_valve_controller import WaterValveOpened

cred = credentials.Certificate(f'{Path.home()}/spikemonitor2021-0d03e7c13108.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


def event_handler(_, event: Event):
    data = vars(event)
    doc_ref = db.collection(event.topic).document(data.pop('id'))
    data['timestamp'] = datetime.datetime.fromisoformat(data['timestamp'])
    doc_ref.set(data)


def main():
    events = (
        TemperatureChanged,
        HumidityChanged,
        LowHumidity,
        HumidityAlarm,
        WaterValveOpened,
        Error
    )
    event_handlers = (EventHandler(e, event_handler) for e in events)
    client = Client('Firestore', event_handlers)
    client.listen()


if __name__ == '__main__':
    main()
