try:
   import cPickle as pickle
except:
   import pickle
import os.path

from taipan.Learning.EntityIdentification.AgdistisIdentifier import AgdistisIdentifier
from taipan.Config.Pathes import cacheFolder

class AgdistisTableIdentifier(object):
    def __init__(self):
        self.agdistis = AgdistisIdentifier()

    def disambiguateTable(self, table):
        cacheFileEntities = os.path.join(cacheFolder, table.id + ".entities.cache")

        if(os.path.exists(cacheFileEntities)):
            entities = pickle.load(open(cacheFileEntities, 'rb'))
        else:
            entities = []
            for row in table.getData():
                entities.append(self.identifyEntitiesForRow(row))
            pickle.dump(entities, open(cacheFileEntities, "wb" ) )

        return entities

    def identifyEntitiesForRow(self, row):
        entitiesRow = []
        for cellIndex, cellValue in enumerate(row):
            entitiesCell = self.agdistis.identifyEntity(cellValue)
            entitiesRow.append(self.agdistis.flattenUrls(entitiesCell))
        return entitiesRow
