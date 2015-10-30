import re

from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class NumberOfDigitsAverage(FeatureInterface):
    def __init__(self):
        self.nonDecimal = re.compile(r'[^\d.]+')

    def calculate(self, column):
        count = 0
        for cell in column:
            filteredCell = self.nonDecimal.sub('', cell)
            count += len(filteredCell)
        return float(count) / len(column)
