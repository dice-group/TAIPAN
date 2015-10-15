import os
try:
   import cPickle as pickle
except:
   import pickle

from taipan.Utils.Exceptions import NoInstancesFoundError
from taipan.Logging.Logger import Logger
from taipan.Config.Pathes import cacheFolder
from taipan.Utils.Exceptions import RelationsDataStructureNotFound

class SimplePropertyMapper(object):
    """
        This class do the property mapping for a given table
        Algorithm 2: Taipan Property Mapping Algorithm
    """

    def __init__(self):
        self.logger = Logger().getLogger(__name__)

    def mapProperties(self, table):
        tableData = table.getData()
        tableHeader = table.getHeader()
        tableId = table.id
        cacheFile = os.path.join(cacheFolder, tableId + ".relations.cache")

        if(os.path.exists(cacheFile)):
            relations = pickle.load(open(cacheFile, 'rb'))
        else:
            raise RelationsDataStructureNotFound("Could not found Rels structure for %s"%(str(tableId),))

        import ipdb; ipdb.set_trace()
