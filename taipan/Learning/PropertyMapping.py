import taipan.Config.Pathes

from taipan.Relational.Atomizers import MannheimAtomizer
from taipan.Search.Solr import SolrSearch

class PropertyMapper(object):
    """
        This class do the property mapping for a given table
    """

    def __init__(self):
        self.mannheimAtomizer = MannheimAtomizer()
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

    def mapProperties(self, table):
        atomicTables = self.mannheimAtomizer.atomizeTable(table)
        annotatedSubjectColumn = self.annotateColumn(atomicTables[0][0])
        for atomicTable in atomicTables:
            annotatedOtherColumn = self.annotateColumn(atomicTable[1])
            for cellnumber in range(len(annotatedSubjectColumn)):
                subjectCell = annotatedSubjectColumn[cellnumber]
                otherCell = annotatedOtherColumn[cellnumber]
                print (subjectCell, otherCell)
