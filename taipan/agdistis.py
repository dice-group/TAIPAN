import re

from agdistispy.agdistis import Agdistis

from taipan.util import clear_string
from taipan.memorize import Memorize

class AgdistisWrapper(object):
    def __init__(self):
        self.agdistis = Agdistis()

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

    def disambiguate_table(self, table):
        entities = []
        for row in table.table:
            entities.append(self.disambiguate_row(row))
        return entities

    def disambiguate_row(self, row):
        entities = []
        for cell_i, cell in enumerate(row):
            cell_entities = self.disambiguate_entity(cell)
            entities.append(self.flatten_urls(cell_entities))
        return entities
