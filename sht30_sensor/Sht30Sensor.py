import adafruit_sht31d
import board


class Sht30Sensor:
    def __init__(self):
        self.sensor = adafruit_sht31d.SHT31D(board.I2C())

    @property
    def temperature(self) -> float:
        return self.sensor.temperature

    @property
    def humidity(self) -> float:
        return self.sensor.relative_humidity
