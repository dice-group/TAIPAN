import re

from agdistispy.agdistis import Agdistis
from foxpy.fox import Fox

from taipan.util import clear_string

class AgdistisWrapper(object):
    def __init__(self):
        self.agdistis = Agdistis()
        self.fox = Fox()

    def flatten_urls(self, entities):
        flattened_urls = []
        for item in entities:
            if item['disambiguatedURL'] != None:
                flattened_urls.append(item['disambiguatedURL'])
        return flattened_urls

    def disambiguate_entity(self, string):
        """
            string: Austria
            [{u'disambiguatedURL': u'http://dbpedia.org/resource/Austria',
              u'namedEntity': u'Austria',
              u'offset': 7,
              u'start': 0}]
        """
        string = clear_string(string)
        return self.agdistis.disambiguateEntity(string)

    def disambiguate(self, string):
        string = clear_string(string)
        return self.agdistis.disambiguate(string)

    def disambiguate_table(self, table):
        entities = []
        for row in table.table:
            entities.append(self.disambiguate_row(row))
        return entities

    def _disambiguate_row(self, row):
        """
            Concat row and disambiguate the complete row
        """
        r_entities = [[]]*len(row)
        row_concat = " ".join(row)
        entities = self.fox.annotateEntities(row_concat)
        d_entities = self.disambiguate(entities)
        for _entity in d_entities:
            for cell_i, cell in enumerate(row):
                if _entity["namedEntity"] in row[cell_i]:
                    r_entities[cell_i] = [_entity["disambiguatedURL"]]
        return r_entities

    def disambiguate_row(self, row):
        """
            Disambiguate cell by cell
            This performs better
        """
        entities = []
        for cell_i, cell in enumerate(row):
            cell_entities = self.disambiguate_entity(cell)
            entities.append(self.flatten_urls(cell_entities))
        return entities
