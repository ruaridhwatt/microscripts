from event_broker import Event, EventField


class OpenWaterValveRequestDenied(Event):
    topic = 'OpenWaterValveRequestDenieds'

    def __init__(self, reason: EventField, **kwargs):
        super().__init__(**kwargs)
        self.reason = reason
