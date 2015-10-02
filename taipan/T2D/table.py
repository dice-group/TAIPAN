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

        #self.tableInstance = self.getTablesInstance(id) #The same as self.table
        #self.attributesInstance = self.getAttributesInstance(id) #The same as self.attributes
        #self.classesInstance = self.getClassesInstance(id) #The same as self.classes

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
        attributes = []
        for row in attributesRaw:
            attribute = {
                "uri": row[0],
                "headerValue": row[1],
                "isKey": False if row[2] == "False" else True,
                "columnIndex": int(row[3])
            }
            attributes.append(attribute)
        return attributes

    def getEntitiesInstance(self, id):
        entitiesRaw = self.loadCsv(os.path.join(t2dDataDir, 'entities_instance', id))
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
        classesRaw = classes[classes[:,0] == id]
        classes = []
        for row in classesRaw:
            _class = {
                "name": row[1],
                "uri": row[2],
                "headerRowIndices": row[3].split(".") #dot separated values
            }
            classes.append(_class)
        return classes

    def loadCsv(self, csvPath):
        if(os.path.exists(csvPath)):
            csv = numpy.genfromtxt(csvPath, delimiter=",", dtype="S", comments="\n")
            for x in numpy.nditer(csv, op_flags=['readwrite']):
                x[...] = str(x).strip('"')
            return csv
        else:
            return []

if __name__ == "__main__":
    sampleId = "39759273_0_1427898308030295194.csv"
    t2dTable = T2DTable(sampleId)
    import ipdb; ipdb.set_trace()
