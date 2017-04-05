from taipan.ml.connectivity import ConnectivityCalculator

class FeatureInterface(object):
    def calculate(self, col, col_i, table):
        raise NotImplemented("Function calculate is not implemented")

class Connectivity(FeatureInterface):
    def __init__(self):
        self.connectivity_calc = ConnectivityCalculator()

    def calculate(self, col, col_i, table):
        connectivity = self.connectivity_calc.get_connectivity(table)
        return connectivity[col_i]
