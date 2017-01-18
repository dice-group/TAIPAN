import unittest

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Learning.SubjectColumnIdentification.SimpleIdentifier import SimpleIdentifier
from taipan.Learning.SubjectColumnIdentification.DistantSupervisionIdentifier import DistantSupervisionIdentifier

from taipan.Logging.Logger import Logger

class SubjectColumnIdentificationBenchTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTable = sampler.getTestTable()
        self.dlIdentifier = DistantSupervisionIdentifier()
        self.simpleIdentifier = SimpleIdentifier()
        #self.testTables20 = sampler.get20Tables()
        #self.testTables = sampler.getTablesSubjectIdentification()

    def testDistantLearningIdentifierNotCorrect(self):
        idList = ["68779923_2_1000046510804975562.csv"]
                  #"9353071_0_969221250383056227.csv",
                  #"94145647_0_4411495338698364870.csv",
                  #"9348099_0_390574653830621671.csv",
                  #"30103516_1_7626625507688323656.csv",
                  #"28788428_0_7847978656182431680.csv",
                  #"39650055_5_7135804139753401681.csv"]

        for _id in idList:
            table = T2DTable(_id)
            support = 1
            connectivity = 4
            threshold = 0
            subjectColumn = self.dlIdentifier.identifySubjectColumn(table, support=support, connectivity=connectivity, threshold=threshold)
            print "subjectColumn %s" % (table.subjectColumn,)
            print "identified %s" % (subjectColumn,)
            print table.table[0:5]
