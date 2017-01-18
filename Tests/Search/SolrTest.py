import unittest

from taipan.Utils.Sampling import Sampler
from taipan.Relational.Parsers import MannheimTable
from taipan.Search.Solr import SolrSearch

class SolrTestCase(unittest.TestCase):
    def setUp(self):
        self.solr = SolrSearch()

    def testGetInstances(self):
        instances = self.solr.getInstances("Batman & Robin")
        self.assertTrue('id' in instances[0], msg="Instance should have 'id' key")
        self.assertTrue('_version_' in instances[0], msg="Instance should have '_version_' key")
        self.assertTrue('comment_en' in instances[0], msg="Instance should have 'comment_en' key")
        self.assertTrue('score' in instances[0], msg="Instance should have 'score_en' key")
