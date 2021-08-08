import operator
import random


class OscillatingFloatProperty:
    def __init__(self, initial_value, min_value, max_value, max_delta):
        self.__value = initial_value
        self.__min_value = min_value
        self.__max_value = max_value
        self.__max_delta = max_delta
        self.__step_operator = operator.iadd

    @property
    def value(self):
        delta = random.uniform(0, self.__max_delta)
        self.__value = self.__step_operator(self.__value, delta)
        if self.__value > self.__max_value:
            self.__value = self.__max_value
            self.__step_operator = operator.isub
        elif self.__value < self.__min_value:
            self.__value = self.__min_value
            self.__step_operator = operator.iadd
        return self.__value
