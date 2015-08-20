import json

from taipan.utils.exceptions import TableHasNoValueError

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

    def getValue(self, valueName):
        if(valueName in self.table):
            return self.table[valueName]
        else:
            raise TableHasNoValueError(valueName)

if __name__ == "__main__":
    from taipan.utils.sampling import Sampler
    sampler = Sampler()
    randomTable = sampler.getRandomTables(1)
    parser = MannheimParser(randomTable[0])
    import ipdb; ipdb.set_trace()
