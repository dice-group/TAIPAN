"""Benchmark for taipan.agdistis"""

from taipan.agdistis import AgdistisWrapper
from taipan.ml.model import MLModel
from taipan.pathes import ENTITIES_DIR, TABLES_DIR
from taipan.generictable import GenericTable

from os import listdir
from os.path import isfile, join

def test_benchmark_agdistis():
    agdistis_wrapper = AgdistisWrapper()
    onlyfiles = [f for f in listdir(ENTITIES_DIR) if isfile(join(ENTITIES_DIR, f))]
    num = 172
    while True:
        try:
            _id = onlyfiles[num]
            print("process table %d out of %d" % (num, len(onlyfiles)), flush=True)
            print("table id %s" % (_id), flush=True)
            fixture_entities = get_gold_standard_entities(_id)
            _table = GenericTable(filename=join(TABLES_DIR, _id),_id=_id)
            _table.init()
            agdistis_entities = agdistis_wrapper.disambiguate_table(_table)
            to_compare = map_agdistis_entities_to_gold_standard_format(_table, agdistis_entities)
            print("", flush=True)
            print(fixture_entities, flush=True)
            print("", flush=True)
            print(to_compare, flush=True)
            print(diff_entities(fixture_entities, to_compare), flush=True)
            num += 1
            if(num >= len(onlyfiles)):
                break
        except BaseException as e:
            print(str(e))

def test_get_gold_standard_entities():
    onlyfiles = [f for f in listdir(ENTITIES_DIR) if isfile(join(ENTITIES_DIR, f))]
    for _f in onlyfiles:
        print(_f)
        fixture_entities = get_gold_standard_entities(_f)

def get_gold_standard_entities(_id):
    entities = []
    _f = open(join(ENTITIES_DIR, _id), 'rU')
    for line in _f.readlines():
        (entity, original_string, line_number) = line.split('","')
        translation_table = dict.fromkeys(map(ord, '"'), None)
        entity = entity.translate(translation_table)
        original_string = original_string.translate(translation_table)
        line_number = line_number.translate(translation_table).strip()
        entities.append([entity, original_string, line_number])
    return entities

def map_agdistis_entities_to_gold_standard_format(table, entities):
    formatted_entities = []
    for row_num, row in enumerate(table.table):
        for cell_num, cell in enumerate(row):
            if(entities[row_num][cell_num] != []):
                for _entity in entities[row_num][cell_num]:
                    formatted_entities.append(
                        [_entity, cell, str(row_num)]
                    )
    return formatted_entities

FIXTURE_ENTITIES = [['http://dbpedia.org/resource/Istanbul_Atat%C3%BCrk_Airport', 'atatürk international airport', '17'],
 ['http://dbpedia.org/resource/Sydney_Airport', 'sydney international airport', '22'],
 ['http://dbpedia.org/resource/Brussels_Airport', 'brussels airport', '29'],
 ['http://dbpedia.org/resource/Miami_International_Airport', 'miami international airport', '28'],
 ['http://dbpedia.org/resource/Kuala_Lumpur_International_Airport', 'kuala lumpur international airport', '18'],
 ['http://dbpedia.org/resource/Dublin_Airport', 'dublin airport', '24'],
 ['http://dbpedia.org/resource/Singapore_Changi_Airport', 'singapore changi airport', '7'],
 ['http://dbpedia.org/resource/Hong_Kong_International_Airport', 'hong kong international airport', '3'],
 ['http://dbpedia.org/resource/Antalya_Airport', 'antalya airport', '23'],
 ['http://dbpedia.org/resource/Munich_Airport', 'munich airport', '13'],
 ['http://dbpedia.org/resource/Madrid%E2%80%93Barajas_Airport', 'madrid-barajas airport', '10'],
 ['http://dbpedia.org/resource/John_F._Kennedy_International_Airport', 'john f. kennedy international airport', '16'],
 ['http://dbpedia.org/resource/Taiwan_Taoyuan_International_Airport', 'taoyuan international airport', '14'],
 ['http://dbpedia.org/resource/Incheon_International_Airport', 'incheon international airport', '8'],
 ['http://dbpedia.org/resource/Dubai_International_Airport', 'dubai international airport', '5'],
 ['http://dbpedia.org/resource/Zurich_Airport', 'zürich airport', '19'],
 ['http://dbpedia.org/resource/Amsterdam_Airport_Schiphol', 'amsterdam airport schiphol', '6'],
 ['http://dbpedia.org/resource/Malpensa_Airport', 'malpensa airport', '25'],
 ['http://dbpedia.org/resource/London_Heathrow_Airport', 'london heathrow airport', '1'],
 ['http://dbpedia.org/resource/Gatwick_Airport', 'london gatwick airport', '12'],
 ['http://dbpedia.org/resource/Charles_de_Gaulle_Airport', 'paris charles de gaulle airport', '2'],
 ['http://dbpedia.org/resource/Narita_International_Airport', 'narita international airport', '9'],
 ['http://dbpedia.org/resource/London_Stansted_Airport', 'london stansted airport', '27'],
 ['http://dbpedia.org/resource/Copenhagen_Airport', 'copenhagen airport', '21'],
 ['http://dbpedia.org/resource/Barcelona%E2%80%93El_Prat_Airport', 'barcelona airport', '26'],
 ['http://dbpedia.org/resource/Leonardo_da_Vinci%E2%80%93Fiumicino_Airport', 'leonardo da vinci airport', '15'],
 ['http://dbpedia.org/resource/Toronto_Pearson_International_Airport', 'toronto pearson international airport', '20'],
 ['http://dbpedia.org/resource/Suvarnabhumi_Airport', 'suvarnabhumi airport', '11'],
 ['http://dbpedia.org/resource/Frankfurt_Airport', 'frankfurt airport', '4'],
 ['http://dbpedia.org/resource/Palma_de_Mallorca_Airport', 'palma de mallorca airport', '30']]


ENTITIES_1 = [['http://dbpedia.org/resource/Age/sex/location', 'location', '0'],
 ['http://dbpedia.org/resource/London_Heathrow_Airport', 'london heathrow airport', '1'],
 ['http://dbpedia.org/resource/Null', 'NULL', '1'],
 ['http://dbpedia.org/resource/Charles_de_Gaulle_Airport', 'paris charles de gaulle airport', '2'],
 ['http://dbpedia.org/resource/Null', 'NULL', '2'],
 ['http://dbpedia.org/resource/Hong_Kong_International_Airport', 'hong kong international airport', '3'],
 ['http://dbpedia.org/resource/Null', 'NULL', '3'],
 ['http://dbpedia.org/resource/Frankfurt_Airport', 'frankfurt airport', '4'],
 ['http://dbpedia.org/resource/Dubai_International_Airport', 'dubai international airport', '5'],
 ['http://dbpedia.org/resource/Amsterdam_Airport_Schiphol', 'amsterdam airport schiphol', '6'],
 ['http://dbpedia.org/resource/Null', 'NULL', '6'],
 ['http://dbpedia.org/resource/Singapore_Changi_Airport', 'singapore changi airport', '7'],
 ['http://dbpedia.org/resource/Null', 'NULL', '7'],
 ['http://dbpedia.org/resource/Incheon_International_Airport', 'incheon international airport', '8'],
 ['http://dbpedia.org/resource/Narita_International_Airport', 'narita international airport', '9'],
 ['http://dbpedia.org/resource/Madrid–Barajas_Airport', 'madrid-barajas airport', '10'],
 ['http://dbpedia.org/resource/Suvarnabhumi_Airport', 'suvarnabhumi airport', '11'],
 ['http://dbpedia.org/resource/Gatwick_Airport', 'london gatwick airport', '12'],
 ['http://dbpedia.org/resource/Null', 'NULL', '12'],
 ['http://dbpedia.org/resource/Munich_Airport', 'munich airport', '13'],
 ['http://dbpedia.org/resource/Null', 'NULL', '13'],
 ['http://dbpedia.org/resource/Taiwan_Taoyuan_International_Airport', 'taoyuan international airport', '14'],
 ['http://dbpedia.org/resource/Null', 'NULL', '14'],
 ['http://dbpedia.org/resource/Leonardo_da_Vinci–Fiumicino_Airport', 'leonardo da vinci airport', '15'],
 ['http://dbpedia.org/resource/John_F._Kennedy_International_Airport', 'john f. kennedy international airport', '16'],
 ['http://dbpedia.org/resource/Null', 'NULL', '16'],
 ['http://dbpedia.org/resource/Istanbul_Atatürk_Airport', 'atatürk international airport', '17'],
 ['http://dbpedia.org/resource/Kuala_Lumpur_International_Airport', 'kuala lumpur international airport', '18'],
 ['http://dbpedia.org/resource/Null', 'NULL', '19'],
 ['http://dbpedia.org/resource/Toronto_Pearson_International_Airport', 'toronto pearson international airport', '20'],
 ['http://dbpedia.org/resource/Copenhagen_Airport', 'copenhagen airport', '21'],
 ['http://dbpedia.org/resource/Null', 'NULL', '21'],
 ['http://dbpedia.org/resource/Sydney_Airport', 'sydney international airport', '22'],
 ['http://dbpedia.org/resource/Dublin_Airport', 'dublin airport', '24'],
 ['http://dbpedia.org/resource/Malpensa_Airport', 'malpensa airport', '25'],
 ['http://dbpedia.org/resource/Barcelona–El_Prat_Airport', 'barcelona airport', '26'],
 ['http://dbpedia.org/resource/London_Stansted_Airport', 'london stansted airport', '27'],
 ['http://dbpedia.org/resource/Null', 'NULL', '27'],
 ['http://dbpedia.org/resource/Miami_International_Airport', 'miami international airport', '28'],
 ['http://dbpedia.org/resource/Brussels_Airport', 'brussels airport', '29'],
 ['http://dbpedia.org/resource/Null', 'NULL', '29'],
 ['http://dbpedia.org/resource/Palma_de_Mallorca_Airport', 'palma de mallorca airport', '30'],
 ['http://dbpedia.org/resource/Null', 'NULL', '30']]

def diff_entities(gold_entities, agdistis_entities):
    recognized = 0
    new_entity = 0
    for _entity in agdistis_entities:
        if _entity in gold_entities:
            recognized += 1
        else:
            new_entity += 1
    #total = len(gold_entities)
    return (recognized, new_entity, len(gold_entities))

def test_diff_entities():
    diff = diff_entities(FIXTURE_ENTITIES, ENTITIES_1)
    assert diff == (24, 19, 30)

def test_calculate_score():
    """
        overall: 26124
        recognized: 3792
        new_entities: 11815
    """
    overall = 0
    recognized_overall = 0
    new_entities_overall = 0
    _f = open("agdistis_benchmark_score")
    for line in _f.readlines():
        try:
            (recognized, new_entities, gold) = eval(line)
        except:
            import ipdb; ipdb.set_trace()
        overall += gold
        recognized_overall += recognized
        new_entities_overall += new_entities
    _f.close()
    import ipdb; ipdb.set_trace()
