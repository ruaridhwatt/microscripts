import adafruit_sht31d
import board

from sht30_sensor.SensorReadError import SensorReadError


class Sht30Sensor:
    def __init__(self):
        self.sensor = adafruit_sht31d.SHT31D(board.I2C())

    @property
    def temperature(self) -> float:
        try:
            return self.sensor.temperature
        except Exception as e:
            raise SensorReadError(str(e))

    @property
    def humidity(self) -> float:
        try:
            return self.sensor.relative_humidity
        except Exception as e:
            raise SensorReadError(str(e))
