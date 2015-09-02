import json

from taipan.Utils.Exceptions import TableHasNoValueError
import numpy

class MannheimParser(object):
    """
        Parse a table from Mannheim Table corpus
        Into neat data structures
    """
    def __init__(self, table):
        self.table = self.decodeTable(table)

    def decodeTable(self, table):
        return json.loads(table)

    def hasHeader(self):
        if('hasHeader' in self.table
            and self.table['hasHeader'] == True):
            return True
        else:
            return False

    def getHeaderPosition(self):
        return self.getValue('headerPosition')

    def getPageTitle(self):
        return self.getValue('pageTitle')

    def getRecordOffset(self):
        return (self.getValue('recordOffset'), self.getValue('recordEndOffset'))

    def getS3Link(self):
        return self.getValue('s3Link')

    def getTableNum(self):
        return self.getValue('tableNum')

    def getTableType(self):
        return self.getValue('tableType')

    def getTermSet(self):
        return self.getValue('termSet')

    def getTitle(self):
        return self.getValue('title')

    def getUrl(self):
        """
            Return the source URL of the table.
        """
        return self.getValue('url')

    def getTable(self):
        return numpy.asarray(self.getValue('relation'))

    def getValue(self, valueName):
        if(valueName in self.table):
            return self.table[valueName]
        else:
            raise TableHasNoValueError(valueName)

if __name__ == "__main__":
    from taipan.Utils.Sampling import Sampler
    sampler = Sampler()
    randomTable = sampler.getRandomTables(1)
    parser = MannheimParser(randomTable[0])

    import ipdb; ipdb.set_trace()
