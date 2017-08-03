"""Test for taipan.dbpedialookup"""

import pprint

pprinter = pprint.PrettyPrinter()

def test_analyze_logs():
    gold_standard = []
    recognized_entities = []
    overall = 0
    with open("dbpedia_lookup_benchmark.out") as f:
        for line in f.readlines():
            if line.startswith("["):
                if not gold_standard:
                    gold_standard = eval(line)
                elif not recognized_entities:
                    recognized_entities = eval(line)
            if gold_standard and recognized_entities:
                diff = diff_entities(gold_standard, recognized_entities)
                diff = filter_entities(diff)
                overall += len(diff)
                #pprinter.pprint(diff)
                gold_standard = []
                recognized_entities = []
    print(overall)

def diff_entities(gold_entities, _entities):
    diff = []
    for _entity in _entities:
        if not _entity in gold_entities:
            diff.append(_entity)
    return diff

def filter_entities(entities):
    filtered = []
    for _entity in entities:
        if not string_only_contain(_entity[1], "1234567890%.&#;") and _entity[1] != "NULL" and len(_entity[1]) > 3:
            filtered.append(_entity)
    return filtered

def test_string_contain():
    assert string_only_contain("4932094", "1234567890%.&#;") == True
    assert string_only_contain("4932094asdf", "1234567890%.&#;") == False
    assert string_only_contain("4932094", "123") == False
    pass

def string_only_contain(_string, characters):
    for char in _string:
        if not char in characters:
            return False
    return True
