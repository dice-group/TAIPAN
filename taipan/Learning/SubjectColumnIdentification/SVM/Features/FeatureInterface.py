from taipan.Utils.Exceptions import NotImplemented

class FeatureInterface(object):
    def calculate(self, column):
        raise NotImplemented("Function calculate is not implemented")
