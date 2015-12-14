import csv
import re

f = open("properties_gold.csv")

tables = {}
for line in f.readlines():
    (tableId, columnIndex, hasProperty, propertyUri) = line.split(",")
    if tableId not in tables:
        tables[tableId] = []
    propertyUri = re.sub("\n", "", propertyUri)
    propertyUri = re.sub("dbpedia-owl:", "http://dbpedia.org/ontology/", propertyUri)
    annotation = {
        'columnIndex': columnIndex,
        'hasProperty': hasProperty,
        'propertyUri': propertyUri
    }
    tables[tableId].append(annotation)

for tableId in tables:
    with open('dbpedia_properties/%s'%(tableId,), 'wb') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        for annotation in tables[tableId]:
            if annotation['propertyUri'] != '':
                row = [annotation['propertyUri'], "", "False",annotation['columnIndex']]
                csvwriter.writerow(row)

fieldnames = ['propertyUri', 'columnIndex', 'hasProperty']
for tableId in tables:
    with open('properties_complete/%s'%(tableId,), 'wb') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csvwriter.writeheader()
        for annotation in tables[tableId]:
            csvwriter.writerow(annotation)
