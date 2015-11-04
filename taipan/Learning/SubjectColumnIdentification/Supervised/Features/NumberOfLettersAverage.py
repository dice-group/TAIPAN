import re

from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class NumberOfLettersAverage(FeatureInterface):
    def __init__(self):
        self.decimal = re.compile(r'[\d.]+')

    def calculate(self, column, columnIndex, table):
        count = 0
        for cell in column:
            filteredCell = self.decimal.sub('', cell)
            count += len(filteredCell)
        return float(count) / len(column)
