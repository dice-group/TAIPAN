from sklearn import svm
import numpy as np
import re


class SVMIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        should have precision of 94%
        Features to use:
        - Fraction of cells with unique content
        - Fraction of cells with numeric content
        - Average number of letters in each cell
        - Average number of numbers in each cell
        - Average number of words in each cell
        - Column index from left
    """
    def __init__(self):
        self.clf = svm.SVC(gamma=0.001, C=100.)
        self.decimal = re.compile(r'[\d.]+')
        self.nonDecimal = re.compile(r'[^\d.]+')
        pass

    def calculateFractionOfCellsWithUniqueContent(self, column):
        return float(len(set(column))) / len(column)

    def calculateFractionOfCellsWithNumericContent(self, column):
        count = 0
        for cell in column:
            filteredCell = self.nonDecimal.sub('', cell)
            if filteredCell == cell:
                count += 1
        return float(count) / len(column)

    def calculateAverageNumberOfLetters(self, column):
        count = 0
        for cell in column:
            filteredCell = self.decimal.sub('', cell)
            count += len(filteredCell)
        return float(count) / len(column)

    def calculateAverageNumberOfNumbers(self, column):
        count = 0
        for cell in column:
            filteredCell = self.nonDecimal.sub('', cell)
            count += len(filteredCell)
        return float(count) / len(column)

    def calculateAverageNumberOfWords(self, column):
        count = 0
        for cell in column:
            count += len(re.findall(r'\w+', cell))
        return float(count) / len(column)

    def calculateFeaturesTable(self, table):
        columns = []
        tableData = table.getData()
        tableColumns = tableData.transpose()
        columnFeatureVectors = []
        targetVector = []
        for columnIndex, column in enumerate(tableColumns):
            columnFeatureVectors.append(self.calculateFeaturesColumn(column, columnIndex))
            targetVector.append(table.isSubjectColumn(columnIndex))
        return (columnFeatureVectors, targetVector)

    def calculateFeaturesColumn(self, column, columnIndex):
        fractionOfCellsUniqueContent = self.calculateFractionOfCellsWithUniqueContent(column)
        fractionOfCellsNumericContent = self.calculateFractionOfCellsWithNumericContent(column)
        numberOfLetters = self.calculateAverageNumberOfLetters(column)
        numberOfNumbers = self.calculateAverageNumberOfNumbers(column)
        numberOfWords = self.calculateAverageNumberOfWords(column)
        featureVector = [fractionOfCellsUniqueContent, fractionOfCellsNumericContent, numberOfLetters, numberOfNumbers, numberOfWords, columnIndex]
        return featureVector

    def calculateFeatures(self):
        from taipan.T2D.Sampler import T2DSampler
        sampler = T2DSampler()
        testTables = sampler.getTablesSubjectIdentification()
        columns = {"data": np.ndarray([]), "target": np.ndarray([])}
        features = []
        target = []
        for table in testTables:
            (columnFeatureVectors, targetVector) = self.calculateFeaturesTable(table)
            features.extend(columnFeatureVectors)
            target.extend(targetVector)

        return (features, target)

    def nFoldValidation(self, fold):
        (data, target) = self.calculateFeatures()
        trainingData = data[:len(data)/fold]
        trainingTarget = target[:len(target)/fold]
        validationData = data[len(data)/fold:]
        validationTarget = target[len(target)/fold:]

        self.clf.fit(trainingData, trainingTarget)

        predictedValues = self.clf.predict(validationData)
        count = 0
        falsePositives = 0
        falseNegatives = 0
        for idx, predictedValue in enumerate(predictedValues):
            if predictedValue == validationTarget[idx]:
                count += 1
            elif predictedValue == True:
                falsePositives += 1
            elif predictedValue == False:
                falseNegatives += 1

        precision = float(count) / len(validationTarget)
        print "precision: %s" % (precision,)
        print "false positives: %s" % (falsePositives,)
        print "false negatives: %s" % (falseNegatives,)

if __name__ == "__main__":
    svm = SVMIdentifier()
    svm.nFoldValidation(3)
