from taipan.config.pathes import tablesFolder

import os
import os.path
import random

class Sampler(object):
    """
        Pick up random tables from the table corpus
    """

    def __init__(self):
        pass

    def getTableFileList(self, withHeaders=True):
        tableFiles = [f for f in os.listdir(tablesFolder) if os.path.isfile(os.path.join(tablesFolder, f))]
        tableFilesWithHeaders = []
        tableFilesWithoutHeaders = []
        for tableFile in tableFiles:
            if(tableFile.endswith("with-headers.json")):
                tableFilesWithHeaders.append(tableFile)
            else:
                tableFilesWithoutHeaders.append(tableFile)
        if(withHeaders):
            return tableFilesWithHeaders
        else:
            return tableFilesWithoutHeaders

    def getRandomTableFile(self, withHeaders=True):
        tableFiles = self.getTableFileList(withHeaders=withHeaders)
        return random.choice(tableFiles)

    def getRandomTables(self, numberOfRandomTables, withHeaders=True):
        tableFile = self.getRandomTableFile(withHeaders=withHeaders)
        tableFilePath = os.path.join(tablesFolder, tableFile)
        tables = open(tableFilePath).readlines()
        randomTables = []
        for i in range(0, numberOfRandomTables):
            randomTables.append(tables[random.randrange(len(tables))])
        return randomTables

if __name__ == "__main__":
    sampler = Sampler()
    table = sampler.getRandomTables(1)
    import ipdb; ipdb.set_trace()
