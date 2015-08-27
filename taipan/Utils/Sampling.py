from taipan.Config.Pathes import tablesDir

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
        tableFiles = [f for f in os.listdir(tablesDir) if os.path.isfile(os.path.join(tablesDir, f))]
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
        tableFilePath = os.path.join(tablesDir, tableFile)
        tables = open(tableFilePath).readlines()
        randomTables = []
        for i in range(0, numberOfRandomTables):
            randomTables.append(tables[random.randrange(len(tables))])
        return randomTables

if __name__ == "__main__":
    sampler = Sampler()
    table = sampler.getRandomTables(1)
    import ipdb; ipdb.set_trace()
