from taipan.Config.Pathes import t2dDataDir
from taipan.T2D.Table import T2DTable
import os.path
import os

class T2DSampler(object):
    def __init__(self):
        pass

    def getListOfTableIds(self):
        tablesCompletePath = os.path.join(t2dDataDir, 'tables_complete')
        ids = [ f for f in os.listdir(tablesCompletePath) if os.path.isfile(os.path.join(tablesCompletePath,f)) ]
        return ids

    def getTable(self, id):
        return T2DTable(id)

    def getTables(self):
        tables = []
        idList = self.getListOfTableIds()
        for id in idList:
            tables.append(self.getTable(id))
        return tables

    def getTestTable(self):
        tableId = "43729470_1_5047305886112599189.csv"
        return self.getTable(tableId)

if __name__ == "__main__":
    t2dSampler = T2DSampler()
    #tables = t2dSampler.getTables()
    table = t2dSampler.getTestTable()
    import ipdb; ipdb.set_trace()
