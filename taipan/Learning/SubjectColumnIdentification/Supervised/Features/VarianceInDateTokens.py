import re

from .FeatureInterface import FeatureInterface

class VarianceInDateTokens(FeatureInterface):
    def __init__(self):
        pass

    def calculate(self, column, columnIndex, table):
        return 0
