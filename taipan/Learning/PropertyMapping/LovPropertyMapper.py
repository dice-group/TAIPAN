import taipan.Config.Pathes
from taipan.Logging.Logger import Logger

from taipan.Learning.PropertyRecommendation.SimplePropertyRecommender import SimplePropertyRecommender

class LovPropertyMapper(object):
    scoreThreshold = 0.8

    def __init__(self, scoreThreshold=0.8):
        self.scoreThreshold = scoreThreshold
        self.logger = Logger().getLogger(__name__)

    def mapProperties(self, table):
        properties = []

        header = table.getHeader()
        propertyRecommender = SimplePropertyRecommender()
        for columnIndex, headerItem in enumerate(header):
            lovProperties = propertyRecommender.lookupPropertiesLOV(headerItem)
            if lovProperties == None:
                continue

            for _property in lovProperties:
                if _property['score'] > self.scoreThreshold:
                    properties.append({"columnIndex": columnIndex, "uri": _property["uri"]})
                    break

        return properties
