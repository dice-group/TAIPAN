import taipan.Config.Pathes

class SimpleIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        This should have precision of 83%
    """
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

class SVMIdentifier(object):
    """
        According to Recovering Semantics of Tables on The Web, 2011
        should have precision of 94%
        Features to use:
        - Fraction of cells with unique content
        - Fraction of cells with numeric content
        - Variance in the number of date tokens in each cell
        - Average number of words in each cell
        - Column index from left
    """
    def __init__(self):
        pass
