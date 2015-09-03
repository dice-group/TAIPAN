import taipan.Config.Pathes

from taipan.Relational.Atomizers import MannheimAtomizer
from taipan.Search.Solr import SolrSearch
from taipan.Search.PropertySearch import PropertySearch
from taipan.Utils.Exceptions import NoInstancesFoundError

class PropertyMapper(object):
    """
        This class do the property mapping for a given table
    """

    def __init__(self):
        self.mannheimAtomizer = MannheimAtomizer()
        self.propertySearch = PropertySearch()
        self.solr = SolrSearch()

    def searchInstanceFor(self, string):
        return self.solr.getInstances(string)

    def annotateColumn(self, column):
        annotatedColumn = []
        for item in column:
            instances = self.searchInstanceFor(item)
            annotatedColumn.append({
                "string": item,
                "instances": instances
            })
        return annotatedColumn

    def searchPropertyFor(self, subjectCell, otherCell):
        #For each instance in subjectCell -- match instance in otherCell
        # if(len(subjectCell['instances']) == 0):
        #     raise NoInstancesFoundError("No instances found for subject cell %s" % subjectCell['string'])
        results = []

        for instance in subjectCell['instances']:
            #Match against string
            results.append(self.propertySearch.searchPropertiesSparql(instance['id'], otherCell['string']))
            for otherInstance in otherCell['instances']:
                results.append(self.propertySearch.searchPropertiesSparql(instance['id'], otherInstance['id']))
        import ipdb; ipdb.set_trace()
        
    def mapProperties(self, table):
        atomicTables = self.mannheimAtomizer.atomizeTable(table)
        annotatedSubjectColumn = self.annotateColumn(atomicTables[0][0])
        for atomicTable in atomicTables:
            annotatedOtherColumn = self.annotateColumn(atomicTable[1])
            for cellnumber in range(len(annotatedSubjectColumn)):
                subjectCell = annotatedSubjectColumn[cellnumber]
                otherCell = annotatedOtherColumn[cellnumber]
                try:
                    self.searchPropertyFor(subjectCell, otherCell)
                except NoInstancesFoundError as e:
                    print str(e)
                    continue
