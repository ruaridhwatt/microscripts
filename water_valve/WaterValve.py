import time

from config import WATER_VALVE_PIN
import gpiozero


class WaterValve:
    def __init__(self):
        self.io = gpiozero.DigitalOutputDevice(WATER_VALVE_PIN, active_high=False, initial_value=None)
        self.io.off()

    def open(self, seconds):
        try:
            self.io.on()
            time.sleep(seconds)
        finally:
            self.io.off()
