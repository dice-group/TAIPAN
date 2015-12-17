import datetime

from pymongo import MongoClient
from .config import connectionString

class MongoLabConnector(object):
    quorum = 2

    def __init__(self):
        self.client = MongoClient(connectionString)
        self.database = self.client.tableannotation
        #https://mongolab.com/databases/propertyannotation#collections

    def getUserAnnotationsCount(self, username):
        paCollection = self.database.PropertyAnnotation
        return paCollection.find({"username": username}).count()

    def getTableUnderConsensus(self, username):
        paCollection = self.database.PropertyAnnotation
        lockCollections = self.database.locks
        annotatedTables = paCollection.find()
        annotatedTableIds = []
        for table in annotatedTables:
            annotatedTableIds.append(table['tableId'])

        annotatedTableIds = list(set(annotatedTableIds))

        for tableId in annotatedTableIds:
            #Overall annotations
            annotations = paCollection.find({"tableId": tableId}).count()
            locks = lockCollections.find({"tableId": tableId}).count()

            myAnnotations = paCollection.find(
                {
                    "tableId": tableId,
                    "username": username
                }
            ).count()
            myLocks = lockCollections.find(
                {
                    "tableId": tableId,
                    "username": username
                }
            ).count()
            if(annotations + locks < self.quorum):
                if(myAnnotations == 0 and myLocks == 0):
                    return tableId

        return None

    def getMyTables(self, username):
        paCollection = self.database.PropertyAnnotation
        myTables = paCollection.find({"username": username})
        myTableIds = []
        for table in myTables:
            myTableIds.append(table['tableId'])
        return myTableIds

    def getAnnotatedTables(self):
        paCollection = self.database.PropertyAnnotation
        annotatedTables = paCollection.find()

        annotatedTableIds = []
        for table in annotatedTables:
            annotatedTableIds.append(table['tableId'])

        annotatedTableIds = list(set(annotatedTableIds))

        annotatedTableIdsComplete = []
        for tableId in annotatedTableIds:
            #Overall annotations
            annotations = paCollection.find({"tableId": tableId}).count()
            if(annotations >= self.quorum):
                annotatedTableIdsComplete.append(tableId)

        return annotatedTableIdsComplete

    def insertPropertyAnnotation(self, propertyAnnotation):
        paCollection = self.database.PropertyAnnotation
        return paCollection.insert(propertyAnnotation)

    def lockTable(self, tableId, username):
        lockCollections = self.database.locks
        lockCollections.ensure_index("createdAt", expireAfterSeconds=5*60)
        lock = {
            "tableId": tableId,
            "username": username,
            "createdAt": datetime.datetime.utcnow()
        }
        return lockCollections.insert(lock)

    def unlockTable(self, tableId, username):
        lockCollections = self.database.locks
        lock = {
            "tableId": tableId,
            "username": username
        }
        return lockCollections.delete_one(lock)

    def insertSubjectColumnAnnotation(self, subjectColumnAnnotation):
        scaCollection = self.database.SubjectColumnAnnotation
        return scaCollection.insert(subjectColumnAnnotation)

    def testInsertPropertyAnnotation(self):
        propertyAnnotation = {
            "tableId": "string",
            "username": "string",
            "annotatedColumns": [
                {
                    "index": 0,
                    "property": "uri",
                    "hasRelation": True
                },
                {
                    "index": 1,
                    "property": "uri",
                    "hasRelation": False
                }
            ]
        }
        self.insertPropertyAnnotation(propertyAnnotation)

    def testSubjectColumnAnnotation(self):
        subjectColumnAnnotation = {
            "tableId": "string",
            "username": "string",
            "tabletype": "string",
            "index": 100500,
            "noSubjectColumn": False
        }
        self.insertSubjectColumnAnnotation(subjectColumnAnnotation)

if __name__ == "__main__":
    mongolab = MongoLabConnector()
    mongolab.getTableUnderConsensus()
