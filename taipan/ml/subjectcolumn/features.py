import re

from taipan.ml.connectivity import ConnectivityCalculator
from taipan.ml.support import SupportCalculator
from taipan.util import DateRecognizer

class FeatureInterface(object):
    def calculate(self, col, col_i, table):
        raise NotImplemented("Function calculate is not implemented")

class Connectivity(FeatureInterface):
    def __init__(self):
        self.connectivity_calc = ConnectivityCalculator()

    def calculate(self, col, col_i, table):
        connectivity = self.connectivity_calc.get_connectivity(table)
        return connectivity[col_i]

class Support(FeatureInterface):
    def __init__(self):
        self.support_calc = SupportCalculator()

    def calculate(self, col, col_i, table):
        support = self.support_calc.get_support(table)
        return support[col_i]

class CellsWithUniqueContentFraction(FeatureInterface):
    def calculate(self, col, col_i, table):
        return float(len(set(col))) / len(col)

class CellsWithNumericContentFraction(FeatureInterface):
    def __init__(self):
        self.non_decimal = re.compile(r'[^\d.]+')

    def calculate(self, col, col_i, table):
        count = 0
        for cell in col:
            filtered_cell = self.non_decimal.sub('', cell)
            if filtered_cell == cell:
                count += 1
        return float(count) / len(col)

class VarianceInDateTokens(FeatureInterface):
    def __init__(self):
        self.date_recognizer = DateRecognizer()

    def calculate(self, col, col_i, table):
        date_token_no = 0
        for cell in col:
            if(self.date_recognizer.is_date(cell)):
                date_token_no += 1
        mean = float(date_token_no) / len(col)
        variance = float(0)
        for cell in col:
            if(self.date_recognizer.is_date(cell)):
                variance += (1 - mean)*(1 - mean)
            else:
                variance += (0 - mean)*(0 - mean)

        variance = variance / len(col)
        return variance

class NumberOfWordsAverage(FeatureInterface):
    def calculate(self, col, col_i, table):
        count = 0
        for cell in col:
            count += len(re.findall(r'\w+', cell))
        return float(count) / len(col)
