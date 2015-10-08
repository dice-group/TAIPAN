from taipan.Config.Pathes import t2dDataDir
import os.path
import numpy

class T2DTable(object):
    def __init__(self, id):
        self.id = id
        self.table = self.getTableComplete(id)
        self.attributes = self.getAttributesComplete(id)
        self.properties = self.attributes
        self.classes = self.getClassesComplete(id)
        self.entities = self.getEntitiesInstance(id)

    def getTableComplete(self, id):
        return self.loadCsv(os.path.join(t2dDataDir, 'tables_complete', id))

    def getTablesInstance(self, id):
        return self.loadCsv(os.path.join(t2dDataDir, 'tables_instance', id))

    def getAttributesComplete(self, id):
        attributesRaw = self.loadCsv(os.path.join(t2dDataDir, 'attributes_complete', id))
        return self.parseAttributes(attributesRaw)

    def getAttributesInstance(self, id):
        attributesRaw = self.loadCsv(os.path.join(t2dDataDir, 'attributes_instance', id))
        return self.parseAttributes(attributesRaw)

    def parseAttributes(self, attributesRaw):
        if attributesRaw == []:
            return []
        attributes = []
        if attributesRaw.ndim > 1:
            for row in attributesRaw:
                attribute = {
                    "uri": row[0],
                    "headerValue": row[1],
                    "isKey": False if row[2] == "False" else True,
                    "columnIndex": int(row[3])
                }
            attributes.append(attribute)
        else:
            row = attributesRaw
            attribute = {
                "uri": row[0],
                "headerValue": row[1],
                "isKey": False if row[2] == "False" else True,
                "columnIndex": int(row[3])
            }
        return attributes

    def getEntitiesInstance(self, id):
        entitiesRaw = self.loadCsv(os.path.join(t2dDataDir, 'entities_instance', id))
        if entitiesRaw == []:
            return []
        entities = []
        for row in entitiesRaw:
            entity = {
                "uri": row[0],
                "keyValue": row[1],
                "rowIndex": int(row[2])
            }
            entities.append(entity)
        return entities

    def getClassesInstance(self, id):
        allClasses = self.loadCsv(os.path.join(t2dDataDir, 'classes_instance.csv'))
        return self.parseClasses(allClasses, id)

    def getClassesComplete(self, id):
        allClasses = self.loadCsv(os.path.join(t2dDataDir, 'classes_complete.csv'))
        return self.parseClasses(allClasses, id)

    def parseClasses(self, classes, id):
        if classes == []:
            return []
        classesRaw = classes[classes[:,0] == id]
        classes = []
        for row in classesRaw:
            _class = {
                "name": row[1],
                "uri": row[2],
                "headerRowIndices": [ int(x) for x in row[3].split(".") ] #dot separated values
            }
            classes.append(_class)
        return classes

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

    def getHeader(self):
        return self.table[0]

    def getData(self):
        return self.table[1:]

    def getHeaderPosition(self):
        return "FIRST_ROW"

    def getTable(self):
        return self.getData()

    def isSubjectColumn(self, columnIndex):
        classIndex = self.getClassIndex()
        if(columnIndex in classIndex):
            return True
        else:
            return False

    def getClassIndex(self):
        return self.classes[0]['headerRowIndices']

if __name__ == "__main__":
    sampleId = "39759273_0_1427898308030295194.csv"
    t2dTable = T2DTable(sampleId)
    import ipdb; ipdb.set_trace()
