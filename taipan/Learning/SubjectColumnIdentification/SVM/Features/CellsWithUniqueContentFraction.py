from taipan.Learning.SubjectColumnIdentification.SVM.Features.FeatureInterface import FeatureInterface

class CellsWithUniqueContentFraction(FeatureInterface):
    def calculate(self, column):
        return float(len(set(column))) / len(column)
