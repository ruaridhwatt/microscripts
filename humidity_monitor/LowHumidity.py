from event_broker import Event


class LowHumidity(Event):
    topic = 'LowHumidityEvents'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
