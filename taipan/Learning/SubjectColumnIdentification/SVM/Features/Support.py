from taipan.Learning.SubjectColumnIdentification.SupportIdentifier import SupportIdentifier

from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class Support(FeatureInterface):
    def __init__(self):
        self.supportIdentifier = SupportIdentifier()

    def calculate(self, column, columnIndex, table):
        support = self.supportIdentifier.getSupport(table)
        return support[columnIndex]
