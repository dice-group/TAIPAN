import numpy

from taipan.Utils.csv import loadCsv

from taipan.Generic.TableInterface import TableInterface

class Table(TableInterface):
    def __init__(self, filepath):
        self.filepath = filepath
        self.table = self.getTableComplete(id)

    def getTableComplete(self, id):
        return loadCsv(os.path.join(t2dDataDir, 'tables_aggregate', id))

    def isSubjectColumn(self, columnIndex):
        if(columnIndex == None):
            columnIndex = -1

        if(hasattr(self, 'columnIndex')):
            columnIndex = self.translateColumnIndex(columnIndex)

        if(columnIndex == self.subjectColumn):
            return True
        else:
            return False

    def isProperty(self, _property):
        (uri, index) = _property
        for localProperty in self.properties:
            if localProperty['uri'] == uri and localProperty['columnIndex'] == index:
               return True

        return False

    def getNumberOfProperties(self):
        return len(self.properties)

    def getClassIndex(self):
        if(len(self.classes) > 0):
            return self.classes[0]['headerRowIndices']
        else:
            return [0]

if __name__ == "__main__":
    sampleId = "39759273_0_1427898308030295194.csv"
    t2dTable = T2DTable(sampleId)
    t2dTable.scrumbleColumns()
    import ipdb; ipdb.set_trace()
