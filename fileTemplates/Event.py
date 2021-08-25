from event_broker import Event, EventField


class ${NAME}(Event):
    topic = '${NAME}Events'
    def __init__(self, ${field_name}: EventField, **kwargs):
        super().__init__(**kwargs)
        self.${field_name} = ${field_name}
