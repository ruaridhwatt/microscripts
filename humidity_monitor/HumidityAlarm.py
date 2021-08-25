from event_broker import Event, EventField


class HumidityAlarm(Event):
    topic = 'HumidityAlarmEvents'

    def __init__(self, humidity: EventField, **kwargs):
        super().__init__(**kwargs)
        self.humidity = humidity
