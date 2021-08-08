from config import is_raspberrypi

if is_raspberrypi():
    from water_valve.WaterValve import WaterValve
else:
    from water_valve.MockWaterValve import MockWaterValve as WaterValve

from water_valve.WaterValveError import WaterValveError
