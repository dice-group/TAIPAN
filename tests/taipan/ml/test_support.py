from taipan.ml.support import SupportCalculator
from taipan.ml.model import MLModel

S_CALC = SupportCalculator()
MLMODEL = MLModel()


ENTITIES = [
    [['http://dbpedia.org/resource/Jeff_Jahn'], [], []],
    [['http://dbpedia.org/resource/Australia'], [], []],
    [['http://dbpedia.org/resource/Bangladesh'], [], []],
    [['http://dbpedia.org/resource/Cambodia'], ['http://dbpedia.org/resource/United_States_Department_of_Defense'], []],
    [['http://dbpedia.org/resource/Canada'], ['http://dbpedia.org/resource/Computer-aided_design'], []],
    [['http://dbpedia.org/resource/France_2'], ['http://dbpedia.org/resource/EUR,_Rome'], []]
]
def test_calculate_support():
    support = S_CALC.calculate_support(ENTITIES)
    assert support == [100.0, 50.0, 0.0]

SUPPORT = [95.0, 75.0, 0.0]
def test_get_support():
    mlmodel = MLModel()
    table = mlmodel.get_tables()[0]
    support = S_CALC.get_support(table)
    assert support == SUPPORT
