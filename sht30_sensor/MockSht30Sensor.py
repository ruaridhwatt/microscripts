from random import random

from sht30_sensor.OscillatingFloatProperty import OscillatingFloatProperty
from sht30_sensor.SensorReadError import SensorReadError


class MockSht30Sensor:
    def __init__(self):
        self.__temperature = OscillatingFloatProperty(20, 19, 24, 0.5)
        self.__humidity = OscillatingFloatProperty(55, 55, 95, 20)

    @property
    def temperature(self) -> float:
        if random() < 0.05:
            raise SensorReadError('Failed to read temperature from SHT30 sensor')
        return self.__temperature.value

    @property
    def humidity(self) -> float:
        if random() < 0.05:
            raise SensorReadError('Failed to read humidity SHT30 sensor')
        return self.__humidity.value
