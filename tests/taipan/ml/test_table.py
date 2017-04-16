"""Test for taipan.table"""

from taipan.ml.table import Table
from numpy import array, array_equal

TABLE_ID = "57790315_0_2715326399585929245.csv"
TABLE_DATA = array([['Name', 'Phone', 'Category'],
       ['Classic Cleaners', '501-623-8680', 'Laundries - Cleaners'],
       ['Curves', '501-915-0633', 'Spas - Beauty'],
       ['Dogwood Tree', '501-922-2686', 'Misc Services'],
       ['Eyecare Specialties', '501-922-5778', 'Eyecare'],
       ['Fit For Life Therapy-wellness', '501-922-1377', 'Misc Services'],
       ['Flower Dome', '501-623-8811', 'Spas - Beauty'],
       ['Music Staff', '501-922-5645', 'Misc Services'],
       ['Sew Perfect', '501-984-6412', 'Apparel'],
       ['Top Nails', '501-984-5778', 'Spas - Beauty'],
       ['Walmart One Hour Photo', '501-318-9733', 'Photography'],
       ['West End Hair Co', '501-922-2855', 'Spas - Beauty']],
      dtype='<U31')
CLASSES = [{'uri': 'http://dbpedia.org/ontology/Company', 'name': 'Company', 'headerRowIndices': [0]}]
PROPERTIES = [{'isKey': True, 'headerValue': 'Name', 'columnIndex': 0, 'uri': 'http://www.w3.org/2000/01/rdf-schema#label'}, {'isKey': False, 'headerValue': 'Category', 'columnIndex': 2, 'uri': 'http://dbpedia.org/ontology/category'}]


def test_get_data():
    table = Table(TABLE_ID)
    table_data = table.get_data(TABLE_ID)
    assert array_equal(table_data, TABLE_DATA)

def test_get_classes():
    table = Table(TABLE_ID)
    classes = table.get_classes(TABLE_ID)
    assert classes == CLASSES

def test_get_properties():
    table = Table(TABLE_ID)
    properties = table.get_properties(TABLE_ID)
    assert properties == PROPERTIES

def test_get_subject_column():
    table = Table(TABLE_ID)
    subject_column = table.get_subject_column(TABLE_ID)
    assert subject_column == 0

def test_get_subject_column_not_exist():
    table = Table(TABLE_ID)
    subject_column = table.get_subject_column("ifosjfoijdsf")
    assert subject_column == None

def test_is_subject_column():
    table = Table(TABLE_ID)
    table.init()
    assert table.is_subject_column(0)

def test_is_subject_column():
    table = Table(TABLE_ID)
    table.init()
    assert table.is_subject_column(1) == False
