from taipan.Learning.SubjectColumnIdentification.ConnectivityIdentifier import ConnectivityIdentifier

from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class Connectivity(FeatureInterface):
    def __init__(self):
        self.connectivityIdentifier = ConnectivityIdentifier()

    def calculate(self, column, columnIndex, table):
        connectivity = self.connectivityIdentifier.getConnectivity(table)
        return connectivity[columnIndex]
