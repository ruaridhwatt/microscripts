from event_broker import Event, EventField


class WaterValveOpened(Event):
    topic = 'WaterValveOpenedEvents'

    def __init__(self, time_seconds: EventField, **kwargs):
        super().__init__(**kwargs)
        self.time_seconds = time_seconds
