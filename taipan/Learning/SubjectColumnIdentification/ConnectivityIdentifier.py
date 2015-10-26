import collections

from taipan.Logging.Logger import Logger
from taipan.Search.PropertyTableSearch import PropertyTableSearch
from taipan.Learning.EntityIdentification.AgdistisTableIdentifier import AgdistisTableIdentifier

class ConnectivityIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.agdistis = AgdistisTableIdentifier()
        self.propertyTableSearch = PropertyTableSearch()

    def calculateConnectivity(self, relations, applyWeights):
        numberOfColumns = len(relations[0])
        numberOfRows = len(relations)

        #If connected, then 1/numberOfColumns, otherwise 0
        #Should be 1 if connected to all other columns
        connectivity = [0]*numberOfColumns
        #count all relations
        for rowIndex, relation in enumerate(relations):
            _weights = [0]*numberOfColumns
            _connectivity = [0]*numberOfColumns
            for columnIndex in relation:
                score = 0
                weight = 0
                for otherColumnIndex in relation[columnIndex]:
                    if len(relation[columnIndex][otherColumnIndex]) > 0:
                        score += 1
                    weight += len(relation[columnIndex][otherColumnIndex])
                score = float(score) / numberOfColumns
                _connectivity[columnIndex] += score
                _weights[columnIndex] += weight

            #Apply weights
            if applyWeights:
                maximumWeight = max(_weights)
                if maximumWeight == 0:
                    connectivity[columnIndex] = _connectivity[columnIndex]
                else:
                    for columnIndex, w in enumerate(_weights):
                        connectivity[columnIndex] = _connectivity[columnIndex] * (float(w) / maximumWeight)

        #Normalize by number of rows
        for columnIndex, _connectivity in enumerate(connectivity):
            connectivity[columnIndex] = float(_connectivity) / numberOfRows

        return connectivity

    def identifySubjectColumn(self, table, applyWeights=False):
        entities = self.agdistis.disambiguateTable(table)
        relations = self.propertyTableSearch.findRelationsForTable(table, entities)
        connectivity = self.calculateConnectivity(relations, applyWeights)
        #Return column with maximum support
        return connectivity.index(max(connectivity))
