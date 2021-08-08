from random import random
from time import sleep

from water_valve.WaterValveError import WaterValveError


class MockWaterValve:

    def open(self, seconds):
        if random() < 0.05:
            raise WaterValveError('Unable to open water valve')
        else:
            sleep(seconds)
