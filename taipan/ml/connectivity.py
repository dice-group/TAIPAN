from taipan.agdistis import AgdistisWrapper
from taipan.sparql.propertysearch import find_properties
from taipan.cache import enable_cache

class ConnectivityCalculator(object):
    def __init__(self):
        self.agdistis = AgdistisWrapper()

    @enable_cache("connectivity")
    def get_connectivity(self, table):
        entities = self.agdistis.disambiguate_table(table)
        properties = find_properties(table, entities)
        return self.calculate_connectivity(properties)

    def calculate_connectivity(self, properties):
        col_no = len(properties[0])
        row_no = len(properties)

        connectivity = [0]*col_no
        for row_i, row in enumerate(properties):
            _connectivity = [0]*col_no
            for col_i in row:
                score = 0
                for b_col_i in row[col_i]:
                    if len(row[col_i][b_col_i]) > 0:
                        score += 1
                score = float(score) / col_no
                _connectivity[col_i] += score

            for col_i in row:
                connectivity[col_i] += _connectivity[col_i]

        for col_i, _connectivity in enumerate(connectivity):
            connectivity[col_i] = float(_connectivity) / row_no

        return connectivity
