import os.path

from taipan.Config.Pathes import t2dDataDir
from taipan.Utils.csv import loadCsv

from taipan.Generic.TableInterface import TableInterface

class T2DTable(TableInterface):
    def __init__(self, id):
        self.id = id
        self.table = self.getTableComplete(id)
        self.classes = self.getClassesComplete(id)
        self.properties = self.getAttributesComplete(id)
        self.propertiesGold = self.getPropertiesGold(id)
        self.subjectColumn = self.getSubjectColumn(id)
        #self.entities = self.getEntitiesInstance(id)

    def getSubjectColumn(self, id):
        csv = loadCsv(os.path.join(t2dDataDir, 'subject_column', 'subject_column_aggregate.csv'))
        return self.parseSubjectColumn(csv, id)

    def parseSubjectColumn(self, csv, id):
        for row in csv:
            if row[0] == id:
                return int(row[1])
        return None

    def getTableComplete(self, id):
        return loadCsv(os.path.join(t2dDataDir, 'tables_aggregate', id))

    def getTablesInstance(self, id):
        return loadCsv(os.path.join(t2dDataDir, 'tables_instance', id))

    def getAttributesComplete(self, id):
        attributesRaw = loadCsv(os.path.join(t2dDataDir, 'attributes_aggregate', id))
        return self.parseAttributes(attributesRaw)

    def getPropertiesGold(self, id):
        attributesRaw = loadCsv(os.path.join(t2dDataDir, 'properties_gold', 'dbpedia_properties_aggregate', id))
        return self.parseAttributes(attributesRaw)

    def getAttributesInstance(self, id):
        attributesRaw = loadCsv(os.path.join(t2dDataDir, 'attributes_instance', id))
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
            attributes.append(attribute)
        return attributes

    def getEntitiesInstance(self, id):
        entitiesRaw = loadCsv(os.path.join(t2dDataDir, 'entities_instance', id))
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
        allClasses = loadCsv(os.path.join(t2dDataDir, 'classes_instance.csv'))
        return self.parseClasses(allClasses, id)

    def getClassesComplete(self, id):
        allClasses = loadCsv(os.path.join(t2dDataDir, 'classes_aggregate.csv'))
        return self.parseClasses(allClasses, id)

    def parseClasses(self, classes, id):
        if classes == []:
            return []
        classesRaw = classes[classes[:,0] == id]
        classes = []
        for row in classesRaw:
            if row[3] == '':
                headerRowIndices = [0]
            else:
                headerRowIndices = [ int(x) for x in row[3].split(".") ]
            _class = {
                "name": row[1],
                "uri": row[2],
                "headerRowIndices": headerRowIndices #dot separated values
            }
            classes.append(_class)
        return classes

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
