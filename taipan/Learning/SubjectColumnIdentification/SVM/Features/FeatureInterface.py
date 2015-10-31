from taipan.Utils.Exceptions import NotImplemented

class FeatureInterface(object):
    def calculate(self, column, columnIndex, table):
        raise NotImplemented("Function calculate is not implemented")
