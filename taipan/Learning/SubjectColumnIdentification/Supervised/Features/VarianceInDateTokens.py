import re

from .FeatureInterface import FeatureInterface
from taipan.Utils.DateRecognizer import DateRecognizer

class VarianceInDateTokens(FeatureInterface):
    def __init__(self):
        self.dateRecognizer = DateRecognizer()

    def calculate(self, column, columnIndex, table):
        dateTokenCount = 0
        for cell in column:
            isDate = self.dateRecognizer.isDate(cell)
            if(isDate):
                dateTokenCount += 1
        mean = float(dateTokenCount) / len(column)
        variance = float(0)
        for cell in column:
            if(self.dateRecognizer.isDate(cell)):
                variance += (1 - mean)*(1 - mean)
            else:
                variance += (0 - mean)*(0 - mean)

        variance = variance / len(column)
        return variance
