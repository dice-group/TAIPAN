import taipan.Config.Pathes
from taipan.Logging.Logger import Logger

from taipan.Learning.PropertyRecommendation.SimplePropertyRecommender import SimplePropertyRecommender
from taipan.Learning.PropertyMapping.SimplePropertyMapper import SimplePropertyMapper

class RankedLovPropertyMapper(object):
    scoreThreshold = 0.8

    def __init__(self, scoreThreshold=0.8):
        self.scoreThreshold = scoreThreshold
        self.logger = Logger().getLogger(__name__)

    def mapProperties(self, table):
        properties = []
        scores = self.getScores(table)

        header = table.getHeader()
        propertyRecommender = SimplePropertyRecommender()
        for columnIndex, headerItem in enumerate(header):
            lovProperties = propertyRecommender.lookupPropertiesLOV(headerItem)
            if lovProperties == None:
                continue

            for _property in lovProperties:
                if len(scores) > 0:
                    taipanScore = scores[columnIndex].get(_property['uri'], 0)*10
                else:
                    taipanScore = 0
                lovScore = _property['score']
                score = float(taipanScore) + lovScore
                if _property['score'] > self.scoreThreshold:
                    properties.append({"columnIndex": columnIndex, "uri": _property["uri"], "lovScore": lovScore, "taipanScore": taipanScore, "score": score})

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

        return propertiesRanked

    def getScores(self, table):
        simplePropertyMapper = SimplePropertyMapper()
        return simplePropertyMapper.getScores(table)
