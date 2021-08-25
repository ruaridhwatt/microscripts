from event_broker import Event, EventField


class TemperatureChanged(Event):
    topic = 'TemperatureChangedEvents'

    def __init__(self, temperature: EventField, **kwargs):
        super().__init__(**kwargs)
        self.temperature = temperature
