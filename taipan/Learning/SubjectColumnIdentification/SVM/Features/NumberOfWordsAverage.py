import re

from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class NumberOfWordsAverage(FeatureInterface):
    def calculate(self, column):
        count = 0
        for cell in column:
            count += len(re.findall(r'\w+', cell))
        return float(count) / len(column)
