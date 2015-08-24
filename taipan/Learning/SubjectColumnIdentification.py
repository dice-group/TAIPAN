import taipan.config.pathes

class SimpleIdentifier(object):
    identificationThreshold = 0.1

    def __init__(self, parser):
        """
            Passing the whole parser object which got access
            to all the metadata on the table
        """
        self.parser = parser

    def identifySubjectColumn(self):
        headerPosition = self.parser.getHeaderPosition()
        table = self.parser.getTable()
        if(headerPosition == "FIRST_ROW"):
            """
                We can iterate through the columns in the table!
                Otherwise, we have to transpose!
            """
        else:
            table = table.T

        for columnNumber, column in enumerate(table):
            columnString = ''.join([element for element in column])
            digitsInString = 0
            for character in columnString:
                if character.isdigit():
                    digitsInString = digitsInString + 1
            digitsRatio = float(digitsInString)/len(columnString)
            if(digitsRatio < self.identificationThreshold):
                return columnNumber

if __name__ == "__main__":
    from taipan.utils.sampling import Sampler
    sampler = Sampler()
    randomTable = sampler.getRandomTables(1)
    from taipan.relational.parsers import MannheimParser
    parser = MannheimParser(randomTable[0])

    si = SimpleIdentifier(parser)
    colNumber = si.identifySubjectColumn()
    print colNumber
