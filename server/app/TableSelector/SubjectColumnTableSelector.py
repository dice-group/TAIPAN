import random

from taipan.T2D.Sampler import T2DSampler
from ../model import GoogleSpreadsheet

class SubjectColumnTableSelector(object):
    def __init__(self):
        self.t2dSampler = T2DSampler()
        self.gSpread = GoogleSpreadsheet()

    def getRandomTable(self):
        identifiedIds = self.getTablesFromGspread()
        identifiedIds = Counter(identifiedIds)
        #Listing only ids which occurs 1 time --> we need 2 times for consensus
        identifiedIds = [_id for _id in identifiedIds if identifiedIds[_id] == 1]
        if len(identifiedIds) == 0:
            return self.t2dSampler.getRandomTable()
        else:
            _id = random.choice(identifiedIds)
            return self.t2dSampler.getTable(_id)

    def getTablesFromGspread(self):
        return self.gSpread.getIdentifiedTables()
