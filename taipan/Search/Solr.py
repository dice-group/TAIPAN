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
            Returns solr.core.Response object
        """
        return self.shortAbstractsSolr.select("comment_en:"+lookupString)

if __name__ == "__main__":
    solrSearch = SolrSearch()
    robin = solrSearch.getInstance("Robin")
    import ipdb; ipdb.set_trace()
