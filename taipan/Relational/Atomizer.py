class MannheimAtomizer(object):
    """
        Atomizes table based on subject column into N
        tables, where N is (number of columns - 1)
    """
    def __init__(self):
        self.table = table
        pass

    def atomizeTable(self, table, subjectColumnNumber):
        pass


if __name__ == "__main__":
    from taipan.Utils.Sampling import Sampler
    sampler = Sampler()
    randomTable = sampler.getRandomTables(1)

    from taipan.Relational.Parsers import MannheimTable
    table = MannheimTable(randomTable[0])

    mannheimAtomizer = MannheimAtomizer(table)
    import ipdb; ipdb.set_trace()
