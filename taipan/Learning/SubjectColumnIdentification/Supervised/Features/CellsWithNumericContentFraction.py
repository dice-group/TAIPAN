import re

from .FeatureInterface import FeatureInterface

class CellsWithNumericContentFraction(FeatureInterface):
    def __init__(self):
        self.nonDecimal = re.compile(r'[^\d.]+')

    def calculate(self, column, columnIndex, table):
        count = 0
        for cell in column:
            filteredCell = self.nonDecimal.sub('', cell)
            if filteredCell == cell:
                count += 1
        return float(count) / len(column)
