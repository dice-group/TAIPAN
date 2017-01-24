import random

class TableInterface(object):
    def getHeader(self):
        if self.table[0].ndim == 0:
            return numpy.array([self.table[0]])
        else:
            return self.table[0]

    def getData(self):
        if self.table[1:].ndim == 1:
            return numpy.array([self.table[1:]])
        else:
            return self.table[1:]

    def getHeaderPosition(self):
        return "FIRST_ROW"

    def swap_cols(self, arr, frm, to):
        try:
            arr[:,[frm, to]] = arr[:,[to, frm]]
        except:
            pass

    def scrumbleColumns(self, times=1000):
        """
            Scrumble the positions of the columns
            Pick two random columns and change their places
        """
        numOfColumns = len(self.table.transpose())
        columnIndex = [i for i in range(0,numOfColumns)]
        for i in range(0, times):
            colA = random.randint(0, numOfColumns - 1)
            colB = colA
            while colB == colA:
                colB = random.randint(0, numOfColumns - 1)
            indexA = columnIndex.index(colA)
            indexB = columnIndex.index(colB)
            columnIndex[indexA] = colB
            columnIndex[indexB] = colA
            self.swap_cols(self.table,colA,colB)
        self.columnIndex = columnIndex

    def getTable(self):
        return self.getData()

    def getColumnIndex(self):
        return self.columnIndex

    def translateColumnIndex(self, columnNumber):
        return self.columnIndex.index(columnNumber)
