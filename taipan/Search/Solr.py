import solr

from taipan.Config.Solr import solrUri
from taipan.Config.Solr import solrShortAbstractsCore

class SolrSearch(object):
    def __init__(self):
        self.shortAbstractsSolr = solr.Solr(solrUri + solrShortAbstractsCore)

    def getInstances(self, lookupString):
        """
            Document in solrShortAbstractsCore has two fields:
            a standard "id" field and
            comment_en field indexed as English text
            Returns top 10 results:
            {
                 u'_version_': 1511204700087648275L,
                 u'comment_en': [u'Damion Scott is a comic book artist and writer, known for his work on books such as Batman, Robin, and Batgirl, Web of Spider-Man, and Duppy. He splits his time between New York and Tokyo, where he founded an art studio that publishes a Japanese comic called Saturday Morning Cartoons or SAM-C.'],
                 u'id': u'http://dbpedia.org/resource/Damion_Scott',
                 u'score': 2.5929914}
            }
        """
        return self.shortAbstractsSolr.select("comment_en:\""+lookupString+"\"").results
