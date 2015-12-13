import json
import csv

f = open("PropertyAnnotation.json", 'rU')
csvFile = open("PropertyAnnotation.csv", 'wb')

fieldnames = ['tableId', 'index', 'hasProperty', 'propertyUri', 'username']
writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
writer.writeheader()

for line in f.readlines():
    dataLine = json.loads(line)
    if(dataLine['annotatedColumns'] == None):
        continue
    for annotatedColumn in dataLine['annotatedColumns']:
        csvLine = {
            'tableId': dataLine['tableId'],
            'index': annotatedColumn['index'],
            'hasProperty': annotatedColumn['hasProperty'],
            'propertyUri': annotatedColumn['propertyUri'],
            'username': dataLine['username']
        }
        writer.writerow(csvLine)

f.close()
