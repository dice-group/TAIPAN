import re

from agdistispy.agdistis import Agdistis

class AgdistisIdentifier(object):
    def __init__(self):
        self.agdistis = Agdistis()

    def flattenUrls(self, entities):
        flattenedUrls = []
        for item in entities:
            if item['disambiguatedURL'] != None:
                flattenedUrls.append(item['disambiguatedURL'])
        return flattenedUrls

    def identifyEntity(self, string):
        """
            string: Austria
            [{u'disambiguatedURL': u'http://dbpedia.org/resource/Austria',
              u'namedEntity': u'Austria',
              u'offset': 7,
              u'start': 0}]
        """
        string = self.clearString(string)
        return self.agdistis.disambiguateEntity(string)

    def clearString(self, string):
        characters = "{}|"
        string = string.translate(None, characters)
        string = re.sub('&nbsp;', '', string)
        string = string.strip()
        return string

if __name__ == "__main__":
    ag = AgdistisIdentifier()
    print ag.identifyEntity("Austria")
