from event_broker import Event, EventField


class HumidityChanged(Event):
    topic = 'HumidityChangedEvents'

    def __init__(self, humidity: EventField, **kwargs):
        super().__init__(**kwargs)
        self.humidity = humidity
