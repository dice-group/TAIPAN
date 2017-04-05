from taipan.agdistis import AgdistisWrapper
from taipan.sparql.propertysearch import find_properties

class ConnectivityCalculator(object):
    def __init__(self):
        self.agdistis = AgdistisWrapper()

    def get_connectivity(self, table):
        entities = self.agdistis.disambiguate_table(table)
        properties = find_properties(table, entities)
        return self.calculate_connectivity(properties)

    def calculate_connectivity(self, properties):
        col_no = len(relations[0])
        row_no = len(relations)

        connectivity = [0]*col_no
        for row_i, _prop in enumerate(properties):
            _connectivity = [0]*col_no
            for col_i in _prop:
                score = 0
                for b_col_i in _prop[col_i]:
                    if len(_prop[col_i][b_col_i]) > 0:
                        score += 1
                score = float(score) / col_no
                _connectivity[col_i] += score

            for col_i, w in enumerate(_weights):
                connectivity[columnIndex] += _connectivity[columnIndex]

        for col_i, _connectivity in enumerate(connectivity):
            connectivity[col_i] = float(_connectivity) / row_no

        return connectivity
