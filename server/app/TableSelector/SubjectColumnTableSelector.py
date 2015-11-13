import random
from collections import Counter

from taipan.T2D.Sampler import T2DSampler
from ..model import GoogleSpreadsheet

class SubjectColumnTableSelector(object):
    #least number of annotation for each table
    #As the first step we do not require any agreement, just annotated is good
    agreementThreshold = 1

    def __init__(self):
        self.t2dSampler = T2DSampler()
        self.gSpread = GoogleSpreadsheet()

    def getTable(self, tableId):
        return self.t2dSampler.getTable(tableId)

    def getRandomTable(self):
        return self.t2dSampler.getTable(getRandomTableId())

    def getRandomTableId(self):
        identifiedIds = self.gSpread.getIdentifiedTableIds()
        identifiedIds = Counter(identifiedIds)
        #Listing only ids which occurs 1 time --> we need 2 times for consensus
        identifiedIds = [_id for _id in identifiedIds if identifiedIds[_id] < self.agreementThreshold]
        if len(identifiedIds) == 0:
            return self.t2dSampler.getRandomTable().id
        else:
            return random.choice(identifiedIds)
