import json
import time
from enum import IntEnum
from pprint import pformat
from typing import Type, Iterable

from paho.mqtt.client import Client as PahoClient, MQTT_ERR_NO_CONN, MQTTMessage

from event_broker.Event import Event
from event_broker.EventHandler import EventHandler
from local_log import get_logger


class QualityOfService(IntEnum):
    DELIVER_AT_MOST_ONE = 0
    DELIVER_AT_LEAST_ONCE = 1
    DELIVER_EXACTLY_ONCE = 2


class MqttConnectionError(RuntimeError):
    pass


class NotConnectedError(RuntimeError):
    pass


class Client:

    def __init__(self, client_id: str, event_handlers: Iterable[EventHandler] = (), ignore_missed_messages=False,
                 quality_of_service=QualityOfService.DELIVER_AT_LEAST_ONCE):

        self.__logger = get_logger(client_id)
        self.__client = PahoClient(client_id, ignore_missed_messages)

        self.__subscriptions = dict((event_handler.event_type.topic, event_handler) for event_handler in event_handlers)
        self.__quality_of_service = quality_of_service

        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message

        self.__client.connect('localhost')

    def emit_event(self, event: Event, quality_of_service=QualityOfService.DELIVER_AT_LEAST_ONCE, retain=False):
        event_dict = vars(event)

        try:
            result = self.__client.publish(
                topic=event.topic,
                payload=json.dumps(event_dict),
                qos=quality_of_service,
                retain=retain
            )
            self.__logger.info(f'Tx {type(event).__name__}:\n{pformat(event_dict)}\nResult: {result}\n')
        except Exception as e:
            self.__logger.error(str(e))

    def __subscribe(self, event_type: Type[Event]):
        self.__logger.info(f'Subscribing to {event_type.topic}')
        result, message_id = self.__client.subscribe(event_type.topic, self.__quality_of_service)
        if result == MQTT_ERR_NO_CONN:
            error_message = 'Cannot subscribe to events before the client is connected!'
            self.__logger.error(error_message)
            raise NotConnectedError(error_message)

    def __on_connect(self, client, userdata, flags, rc, properties=None):
        class ConnectionResult(IntEnum):
            SUCCESS = 0
            INCORRECT_PROTOCOL_VERSION = 1
            INVALID_CLIENT_ID = 2
            SERVER_UNAVAILABLE = 3
            BAD_USERNAME_OR_PASSWORD = 4
            NOT_AUTHORIZED = 5

        error_messages = {
            ConnectionResult.INCORRECT_PROTOCOL_VERSION: 'Incorrect protocol version',
            ConnectionResult.INVALID_CLIENT_ID: 'Invalid client ID',
            ConnectionResult.SERVER_UNAVAILABLE: 'Mqtt server unavailable',
            ConnectionResult.BAD_USERNAME_OR_PASSWORD: 'Bad username or password',
            ConnectionResult.NOT_AUTHORIZED: 'Not authorized'
        }

        if rc != ConnectionResult.SUCCESS:
            self.__logger.error(error_messages[rc])
            raise MqttConnectionError(error_messages[rc])
        self.__logger.info('Connected')

        for event_handler in self.__subscriptions.values():
            self.__subscribe(event_handler.event_type)

    def __on_message(self, client, userdata, message: MQTTMessage):
        event_handler = self.__subscriptions[message.topic]
        event_dict = json.loads(message.payload)
        event = event_handler.event_type(**event_dict)
        self.__logger.info(f'Rx {event_handler.event_type.__name__}:\n{pformat(event_dict)}\n')
        event_handler.callback(self, event)

    def idle(self, seconds: int):
        for _ in range(seconds):
            self.__idle_1s()

    def __idle_1s(self):
        start = time.time()
        self.__client.loop(1)
        elapsed = time.time() - start
        remainder = max(1 - elapsed, 0)
        time.sleep(remainder)

    def listen(self):
        self.__client.loop_forever()
