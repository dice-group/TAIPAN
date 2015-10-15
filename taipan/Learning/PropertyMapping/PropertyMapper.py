import taipan.Config.Pathes

from taipan.Relational.Atomizers import MannheimAtomizer
from taipan.Search.Solr import SolrSearch
from taipan.Search.PropertySearch import PropertySearch
from taipan.Utils.Exceptions import NoInstancesFoundError
from taipan.Logging.Logger import Logger

class PropertyMapper(object):
    """
        This class do the property mapping for a given table
        I just keep this here for historic reasons, have to clean up later
        This class is not used anywhere for the approach described in WWW paper
    """

    def __init__(self):
        self.mannheimAtomizer = MannheimAtomizer()
        self.propertySearch = PropertySearch()
        self.solr = SolrSearch()
        self.logger = Logger().getLogger(__name__)

    def searchInstanceFor(self, string):
        return self.solr.getInstances(string)

    def annotateColumn(self, column):
        annotatedColumn = []
        for item in column:
            self.logger.debug("Looking for annotations for item: %s" %(item,))
            instances = self.searchInstanceFor(item)
            self.logger.debug("Founded instances: %s" %(instances,))
            annotatedColumn.append({
                "string": item,
                "instances": instances
            })
        return annotatedColumn

    def searchPropertyFor(self, subjectCell, otherCell):
        results = []

        for instance in subjectCell['instances']:
            self.logger.debug("Matching instance %s from subjectCell %s" %(instance, subjectCell['string']))
            #Match against string
            self.logger.debug("Matching against %s" %(otherCell['string'],))
            results.append(self.propertySearch.searchPropertiesSparql(instance['id'], otherCell['string']))
            for otherInstance in otherCell['instances']:
                self.logger.debug("Matching against %s" %(otherInstance,))
                results.append(self.propertySearch.searchPropertiesSparql(instance['id'], otherInstance['id']))
        import ipdb; ipdb.set_trace()

    def mapProperties(self, table):
        atomicTables = self.mannheimAtomizer.atomizeTable(table)
        import ipdb; ipdb.set_trace()
        annotatedSubjectColumn = self.annotateColumn(atomicTables[0][0])

        for atomicTable in atomicTables:
            annotatedOtherColumn = self.annotateColumn(atomicTable[1])
            for cellnumber in range(1, len(annotatedSubjectColumn)):
                subjectCell = annotatedSubjectColumn[cellnumber]
                otherCell = annotatedOtherColumn[cellnumber]
                try:
                    self.searchPropertyFor(subjectCell, otherCell)
                except NoInstancesFoundError as e:
                    print str(e)
                    continue
