from event_broker import Event, EventField


class SensorReading(Event):
    topic = 'SensorReadings'

    def __init__(self, temperature: EventField, humidity: EventField, **kwargs):
        super().__init__(**kwargs)
        self.temperature = round(temperature, 2)
        self.humidity = round(humidity, 3)
