import operator

import taipan.Config.Pathes
from taipan.Logging.Logger import Logger

from taipan.Learning.PropertyRecommendation.SimplePropertyRecommender import SimplePropertyRecommender
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

class RankedLovPropertyMapper(object):
    scoreThreshold = 0.8 #from 0 to 2

    def __init__(self, scoreThreshold=0.8):
        self.scoreThreshold = scoreThreshold
        self.logger = Logger().getLogger(__name__)

    def mergeLovAndTaipanProperties(self, lovProperties, taipanProperties):
        normalizedLovProperties = self.normalizeProperties(lovProperties)
        convertedTaipanProps = self.convertTaipanToLovFormat(taipanProperties)
        normalizedTaipanProperties = self.normalizeProperties(convertedTaipanProps)
        flatLovProps = self.flattenProperties(normalizedLovProperties)
        flatTaipanProps = self.flattenProperties(normalizedTaipanProperties)

        lovWeight = 1
        taipanWeight = 0.5

        mergedProperties = {}
        for _prop in flatLovProps:
            if _prop in flatTaipanProps:
                mergedProperties[_prop] = lovWeight*flatLovProps[_prop] + taipanWeight*flatTaipanProps[_prop]
            else:
                mergedProperties[_prop] = lovWeight*flatLovProps[_prop]

        for _prop in flatTaipanProps:
            if _prop in flatLovProps:
                continue
            else:
                mergedProperties[_prop] = taipanWeight*flatTaipanProps[_prop]

        if len(mergedProperties) == 0:
            return []

        maxScore = max(mergedProperties.iteritems(), key=operator.itemgetter(1))[1]
        normalizedMergedProperties = {}
        for _prop in mergedProperties:
            normalizedMergedProperties[_prop] = mergedProperties[_prop] / maxScore

        return normalizedMergedProperties

    def flattenProperties(self, properties):
        flatProps = {}
        for _prop in properties:
            flatProps[_prop["uri"]] = _prop["score"]
        return flatProps

    def convertTaipanToLovFormat(self, taipanProperties):
        convProperties = []
        for (_propertyUri, score) in taipanProperties.iteritems():
            _prop = {
                "prefixedName": "",
                "score": float(score),
                "uri": _propertyUri
            }
            convProperties.append(_prop)
        return convProperties

    def normalizeProperties(self, properties):
        normalizedLovProperties = []
        maxScore = 0
        for _prop in properties:
            if _prop['score'] > maxScore:
                maxScore = _prop['score']

        for _prop in properties:
            _prop['score'] = _prop['score'] / maxScore
            normalizedLovProperties.append(_prop)

        return normalizedLovProperties

    def mapProperties(self, table):
        properties = []
        scores = self.getScores(table)

        header = table.getHeader()
        propertyRecommender = SimplePropertyRecommender()
        for columnIndex, headerItem in enumerate(header):
            if columnIndex == table.subjectColumn:
                properties.append({"columnIndex": columnIndex, "uri": "http://www.w3.org/2000/01/rdf-schema#label", "lovScore": None, "taipanScore": None, "score": 1.0})
                continue
            lovProperties = propertyRecommender.lookupPropertiesLOV(headerItem)
            _columnProperties = self.mergeLovAndTaipanProperties(lovProperties, scores[columnIndex])

            for _property in _columnProperties:
                if _columnProperties[_property] > self.scoreThreshold:
                    properties.append({"columnIndex": columnIndex, "uri": _property, "lovScore": None, "taipanScore": None, "score": _columnProperties[_property]})

        #filter properties with maximum scores
        propertiesRanked = []
        for columnIndex, headerItem in enumerate(header):
            #get all properties with the same columnIndex
            columnIndexProperties = []
            for _property in properties:
                if _property['columnIndex'] == columnIndex:
                    columnIndexProperties.append(_property)

            if len(columnIndexProperties) == 0:
                continue

            propertiesRanked.append(max(columnIndexProperties, key=lambda x: x['score']))

        return (propertiesRanked, properties)

    def getScores(self, table):
        simplePropertyMapper = SimplePropertyMapper()
        return simplePropertyMapper.getScores(table)
