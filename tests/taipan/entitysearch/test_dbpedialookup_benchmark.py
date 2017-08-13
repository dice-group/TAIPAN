"""Benchmark for taipan.agdistis"""

from nose.tools import nottest

from taipan.ml.model import MLModel
from taipan.ml.subjectcolumn.scidentifier import SCIdentifier
from taipan.pathes import ENTITIES_DIR, TABLES_DIR
from taipan.generictable import GenericTable
from taipan.entitysearch.dbpedialookup import disambiguate_table, \
    disambiguate_table_subject_column_only

from os import listdir
from os.path import isfile, join

@nottest
def test_benchmark_dbpedia_lookup_subject_columns_only():
    onlyfiles = [f for f in listdir(ENTITIES_DIR) if isfile(join(ENTITIES_DIR, f))]
    scidentifier = SCIdentifier()
    num = 0
    while True:
        try:
            _id = onlyfiles[num]
            print("process table %d out of %d" % (num, len(onlyfiles)), flush=True)
            print("table id %s" % (_id), flush=True)
            fixture_entities = get_gold_standard_entities(_id)
            _table = GenericTable(filename=join(TABLES_DIR, _id),_id=_id)
            _table.init()
            _subject_columns = scidentifier.identify_subject_column(_table)
            if _subject_columns:
                _table.subject_column = _subject_columns[0]
            dbpedia_lookup_entities = disambiguate_table_subject_column_only(_table)
            to_compare = map_agdistis_entities_to_gold_standard_format(_table, dbpedia_lookup_entities)
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

@nottest
def test_benchmark_dbpedia_lookup():
    onlyfiles = [f for f in listdir(ENTITIES_DIR) if isfile(join(ENTITIES_DIR, f))]
    num = 0
    while True:
        try:
            _id = onlyfiles[num]
            print("process table %d out of %d" % (num, len(onlyfiles)), flush=True)
            print("table id %s" % (_id), flush=True)
            fixture_entities = get_gold_standard_entities(_id)
            _table = GenericTable(filename=join(TABLES_DIR, _id),_id=_id)
            _table.init()
            dbpedia_lookup_entities = disambiguate_table(_table)
            to_compare = map_agdistis_entities_to_gold_standard_format(_table, dbpedia_lookup_entities)
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

def test_calculate_score():
    """
        for every cell:
        overall: 26124
        recognized: 18361
        new_entities: 85900
        recall: 70.28%

        Only subject column:
        recognized: 15757
        new_entities: 6134
        recall: 60.3%
    """
    overall = 0
    recognized_overall = 0
    new_entities_overall = 0
    _f = open("dbpedia_lookup_benchmark_sc_only_score")
    for line in _f.readlines():
        try:
            (recognized, new_entities, gold) = eval(line)
        except:
            import ipdb; ipdb.set_trace()
        overall += gold
        recognized_overall += recognized
        new_entities_overall += new_entities
    _f.close()
