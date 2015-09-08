from taipan.Relational.Parsers import MannheimTable

class MannheimTables(object):
    def __init__(self, tables):
        self.tables = self.decodeTables(tables)

    def decodeTables(self, tables):
        mannheimTables = []
        for table in tables:
            mannheimTables.append(MannheimTable(table))
        return mannheimTables
