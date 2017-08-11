from taipan.entitysearch.agdistis import AgdistisWrapper
from taipan.cache import enable_cache

class SupportCalculator(object):
    def __init__(self):
        self.agdistis = AgdistisWrapper()

    def calculate_support(self, entities):
        """
            support -- percentage of entities to occur in a column to be considered a candidate for a subject column (columns without entities are not subject column per definition)
        """
        col_no = len(entities[0])
        row_no = len(entities)
        support = [0]*col_no
        for row_i, row in enumerate(entities):
            for col_i, entity in enumerate(row):
                if(len(entity) > 0):
                    support[col_i] += 1

        for col_i, _value in enumerate(support):
            support[col_i] = float(_value) / row_no * 100

        return support

    @enable_cache("support")
    def get_support(self, table):
        entities = self.agdistis.disambiguate_table(table)
        return self.calculate_support(entities)
