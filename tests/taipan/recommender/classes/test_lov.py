from taipan.recommender.classes.lov import get_table_class

TEST_SEARCH_TERM = "person"
TEST_CLASS = {'prefixed_name': 'foaf:Person', 'score': 0.75813615, 'uri': 'http://xmlns.com/foaf/0.1/Person'}

def test_get_table_class():
    classes = get_table_class(TEST_SEARCH_TERM)
    assert TEST_CLASS in classes
