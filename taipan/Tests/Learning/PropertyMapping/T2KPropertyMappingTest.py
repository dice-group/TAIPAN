import unittest
import logging
import os
import numpy
import re

from taipan.T2D.Sampler import T2DSampler
from taipan.T2D.Table import T2DTable
from taipan.Config.Pathes import t2dDataDir

class T2KPropertyMappingTestCase(unittest.TestCase):
    def setUp(self):
        sampler = T2DSampler()
        self.testTables = sampler.getTablesPropertyAnnotationDbpediaGoldStandard()

    def readCsv(self, csvPath):
        if(os.path.exists(csvPath)):
            csv = numpy.genfromtxt(csvPath, delimiter=",", dtype="S", comments="///", missing_values="NULL")
            if numpy.shape(csv) != (0,):
                for x in numpy.nditer(csv, op_flags=['readwrite']):
                    x[...] = str(x).strip('"')
                return csv
            else:
                return []
        else:
            return []

    def getT2KResult(self, tableId):
        """
            Results were precomputed on 128 GB VM
        """
        t2kProperties = os.path.join(t2dDataDir, 'properties_t2k', tableId)
        attributesRaw = self.readCsv(t2kProperties)
        if attributesRaw == []:
            return []
        attributesRaw = attributesRaw[1:]

        if attributesRaw.ndim == 1:
            return []

        attributes = []
        for row in attributesRaw:
            attribute = {
                "uri": row[1],
                "headerValue": row[0],
                "similarityScore": row[2],
                "correct": row[3]
            }
            attributes.append(attribute)
        return attributes

    def restoreColumnIndex(self, properties, table):
        propertiesWithColumnIndex = []
        tableHeader = table.getHeader()
        for _property in properties:
            for columnIndex, _header in enumerate(tableHeader):
                _header = re.sub("&nbsp;", "", _header)
                if _header == "state / province":
                    _header = "state"
                if re.match(_header, _property['headerValue'], re.I|re.U) or _header == _property['headerValue'] or _header.lower() == _property['headerValue'].lower():
                    _property['columnIndex'] = columnIndex
                    propertiesWithColumnIndex.append(_property)
                    break

        if len(properties) != len(propertiesWithColumnIndex):
            raise BaseException

        return propertiesWithColumnIndex

    def testMapProperties(self):
        logging.disable(logging.DEBUG)
        logging.disable(logging.INFO)
        for num, table in enumerate(self.testTables):
            properties = self.getT2KResult(table.id)
            properties = self.restoreColumnIndex(properties, table)
            (overall, correct) = self.diffProperties(properties, table.propertiesGold)
            print "%s, %s" % (overall, correct,)

    def diffProperties(self, propertiesMapped, propertiesGold):
        correct = 0
        overall = len(propertiesMapped)
        for propertyMapped in propertiesMapped:
            #find property with the same columnIndex
            for propertyGold in propertiesGold:
                if propertyMapped['columnIndex'] == propertyGold['columnIndex']:
                    if propertyMapped['uri'] == propertyGold['uri']:
                        correct += 1
        return (overall, correct)
