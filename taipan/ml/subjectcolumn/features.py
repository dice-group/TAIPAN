from taipan.ml.connectivity import ConnectivityCalculator
from taipan.ml.support import SupportCalculator

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

    def calculate(self, column, columnIndex, table):
        support = self.support_calc.get_support(table)
        return support[columnIndex]
