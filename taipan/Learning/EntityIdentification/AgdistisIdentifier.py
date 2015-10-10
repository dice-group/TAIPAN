from agdistispy.agdistis import Agdistis

class AgdistisIdentifier(object):
    def __init__(self):
        self.agdistis = Agdistis()

    def identifyEntity(self, string):
        """
            string: Austria
            [{u'disambiguatedURL': u'http://dbpedia.org/resource/Austria',
              u'namedEntity': u'Austria',
              u'offset': 7,
              u'start': 0}]
        """
        return self.agdistis.disambiguateEntity(string)
