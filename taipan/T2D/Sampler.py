from taipan.Config.Pathes import t2dDataDir
from taipan.T2D.Table import T2DTable
import os.path
import os
import numpy
import random

class T2DSampler(object):
    blackList = [
        "41612329_0_7158224623202100303.csv" #too much inconsistency
    ]
    def __init__(self):
        pass

    def getListOfTableIds(self):
        tablesCompletePath = os.path.join(t2dDataDir, 'tables_complete')
        ids = [ f for f in os.listdir(tablesCompletePath) if os.path.isfile(os.path.join(tablesCompletePath,f)) ]
        return ids

    def getRandomTable(self):
        ids = self.getListOfTableIds()
        _id = random.choice(ids)
        return self.getTable(_id)

    def getListOfTableIdsWithClasses(self):
        allClasses = self.loadCsv(os.path.join(t2dDataDir, 'classes_complete.csv'))
        idList = []
        for row in allClasses:
            idList.append(row[0])
        return idList

    def getTable(self, id):
        return T2DTable(id)

    def getTables(self):
        tables = []
        idList = self.getListOfTableIds()
        for id in idList:
            tables.append(self.getTable(id))
        return tables

    def getTablesSubjectIdentification(self):
        tables = []
        idList = self.loadCsv(os.path.join(t2dDataDir, 'subject_column.csv'))
        for row in idList:
            _id = row[0]
            tables.append(self.getTable(_id))
        return tables

    def getTablesSubjectIdentificationIds(self):
        idList = self.loadCsv(os.path.join(t2dDataDir, 'subject_column.csv'))
        return map((lambda x: x[0]), idList)

    def get20Tables(self):
        tables = []
        idList = self.getListOfTableIds()
        for ix, id in enumerate(idList):
            tables.append(self.getTable(id))
            if ix > 20:
                break
        return tables

    def getTestTable(self):
        tableId = "43729470_1_5047305886112599189.csv"
        #tableId = "75022277_0_6693812820589580743.csv"
        #tableId = "64453534_0_2231985329462980688.csv"
        return self.getTable(tableId)

    def loadCsv(self, csvPath):
        #print csvPath
        if(os.path.exists(csvPath)):
            csv = numpy.genfromtxt(csvPath, delimiter=",", dtype="S", comments="///")
            if numpy.shape(csv) != (0,):
                for x in numpy.nditer(csv, op_flags=['readwrite']):
                    x[...] = str(x).strip('"')
                return csv
            else:
                return []
        else:
            return []

if __name__ == "__main__":
    t2dSampler = T2DSampler()
    #tables = t2dSampler.getTables()
    table = t2dSampler.getTestTable()
    import ipdb; ipdb.set_trace()
