import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier

from taipan.Logging.Logger import Logger

# class SimpleIdentifierBenchTestCase(unittest.TestCase):
#     def setUp(self):
#         sampler = T2DSampler()
#         self.testTable = sampler.getTestTable()
#         self.simpleIdentifier = SimpleIdentifier()

    # def testSimpleColumnIdentifierOne(self):
    #     colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
    #     self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")

class SubjectColumnIdentificationBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.dlIdentifier = DistantSupervisionIdentifier()
        self.simpleIdentifier = SimpleIdentifier()
        # self.testTables20 = sampler.get20Tables()
        self.testTables = sampler.getTablesSubjectIdentification()

    # def testDistantLearningIdentifierOne(self):
    #     colNumber = self.dlIdentifier.identifySubjectColumn(self.testTable)
    #     self.assertTrue(self.testTable.isSubjectColumn(colNumber), msg="colNumber should be subject column")

    # def testDistantLearningIdentifierProblematic(self):
    #     tableId = "65842312_0_4733067625464702086.csv" #Got ???? symbols in the cells
    #     tableId = "95942871_9_1442908185816138298.csv" #utf-8 can not encode char
    #     table = T2DTable(tableId)
    #     colNumber = self.dlIdentifier.identifySubjectColumn(table)

    # def testDistantLearningIdentifierTwenty(self):
    #     print "Analyzing %s tables" % (len(self.testTables20),)
    #     overall = len(self.testTables20)
    #     correct = 0
    #     for table in self.testTables20:
    #         colNumber = self.dlIdentifier.identifySubjectColumn(table)
    #         if(table.isSubjectColumn(colNumber)):
    #             correct += 1
    #
    #     precision = float(correct)/overall
    #     print "Tables analyzed: %s\nSubject Column Identified Correctly: %s\nPrecision: %s" % (overall, correct, precision,)
    #
    def testDistantLearningIdentifierAll(self):
        """
            Tables analyzed: 900
            Subject Column Identified Correctly: 762
            Precision: 0.846666666667
        """
        print "Analyzing %s tables" % (len(self.testTables),)
        overall = 900
        correct = 0
        for table in self.testTables[:900]:
            colNumber = self.dlIdentifier.identifySubjectColumn(table)
            if(table.isSubjectColumn(colNumber)):
                correct += 1

        precision = float(correct)/overall
        print "Tables analyzed: %s\nSubject Column Identified Correctly: %s\nPrecision: %s" % (overall, correct, precision,)

    def testSimpleColumnIdentifierAll(self):
        """
            Tables analyzed: 900
            Subject Column Identified Correctly: 893
            Precision: 0.992222222222
        """
        overall = 900
        correct = 0
        for table in self.testTables[:900]:
            colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
            if(table.isSubjectColumn(colNumber)):
                correct += 1
        precision = float(correct)/overall
        print "Tables analyzed: %s\nSubject Column Identified Correctly: %s\nPrecision: %s" % (overall, correct, precision,)

    def testSimpleColumnIdentifierScrumblingAll(self):
        """
            Tables analyzed: 900
            Subject Column Identified Correctly: 325
            Precision: 0.361111111111
        """
        overall = 900
        correct = 0
        for table in self.testTables[:900]:
            table.scrumbleColumns()
            colNumber = self.simpleIdentifier.identifySubjectColumn(self.testTable)
            colNumber = table.translateColumnIndex(colNumber)
            if(table.isSubjectColumn(colNumber)):
                correct += 1
        precision = float(correct)/overall
        print "Scrumbled Columns"
        print "Tables analyzed: %s\nSubject Column Identified Correctly: %s\nPrecision: %s" % (overall, correct, precision,)
