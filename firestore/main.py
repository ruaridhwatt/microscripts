import datetime
from pathlib import Path

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

from event_broker import Client, Event, EventHandler, ErrorEvent
from humidity_monitor import OpenWaterValveRequest
from sht30_sensor_reader import SensorReading
from water_valve_request_monitor import WaterValveOpenedEvent, OpenWaterValveRequestDenied
print(f'{Path.home()}/spikemonitor2021-0d03e7c13108.json')
cred = credentials.Certificate(f'{Path.home()}/spikemonitor2021-0d03e7c13108.json')
firebase_admin.initialize_app(cred)

db = firestore.client()


def event_handler(client: Client, event: Event):
    data = vars(event)
    doc_ref = db.collection(event.topic).document(data.pop('id'))
    data['timestamp'] = datetime.datetime.fromisoformat(data['timestamp'])
    doc_ref.set(data)


def main():
    events = (SensorReading, OpenWaterValveRequest, WaterValveOpenedEvent, OpenWaterValveRequestDenied, ErrorEvent)
    event_handlers = (EventHandler(e, event_handler) for e in events)
    client = Client('Firestore', event_handlers)
    client.listen()


if __name__ == '__main__':
    main()
