from taipan.Logging.Logger import Logger
from taipan.Config.Pathes import cacheFolder
from taipan.Search.PropertySearch import PropertySearchDbpediaSparql

class PropertyTableSearch(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)

    def findRelationsForTable(self, table, entities):
        cacheFileRelations = os.path.join(cacheFolder, tableId + ".relations.cache")
        tableData = table.getData()

        if(os.path.exists(cacheFileRelations)):
            relations = pickle.load(open(cacheFileRelations, 'rb'))
        else:
            relations = []
            for rowIndex, row in enumerate(tableData):
                rowRels = collections.defaultdict(dict)
                for columnIndex, columnValue in enumerate(row):
                    entity = entities[rowIndex][columnIndex]
                    for otherColumnIndex, otherColumnValue in enumerate(row[columnIndex:]):
                        otherColumnIndex = columnIndex + otherColumnIndex
                        if(row[columnIndex] == row[otherColumnIndex]):
                            rowRels[columnIndex][otherColumnIndex] = []
                        else:
                            rel = self.findRelation(columnValue, otherColumnValue, entities[rowIndex][columnIndex], entities[rowIndex][otherColumnIndex])
                            rowRels[columnIndex][otherColumnIndex] = rel
                            rowRels[otherColumnIndex][columnIndex] = rel
                relations.append(dict(rowRels))
            #save cache
            pickle.dump(relations, open(cacheFileRelations, "wb" ) )
        return relations

    def findRelation(self, columnValue1, columnValue2, entities1, entities2):
        propertySearch = PropertySearchDbpediaSparql()
        properties = []

        if(len(entities1) > 0):
            for entity1 in entities1:
                properties.append(propertySearch.uriLiteralSearch(entity1,columnValue2))
        elif(len(entities2) > 0):
            for entity2 in entities2:
                properties.append(propertySearch.uriLiteralSearch(entity2,columnValue1))
        elif(len(entities1) > 0 and len(entities2) > 0):
            for entity1 in entities1:
                for entity2 in entities2:
                    properties.append(propertySearch.uriUriSearch(entity1, entity2))
        else:
            #both are literals, do nothing
            pass

        #flatten
        properties = [prop for sublist in properties for prop in sublist]
        #remove duplicates
        properties = list(set(properties))

        return properties
