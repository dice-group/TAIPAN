import os

from taipan.util import load_csv
from taipan.pathes import TABLES_DIR, CLASSES_LIST, \
        PROPERTIES_DIR, SUBJECT_COLUMN_LIST, ENTITIES_DIR

class Table(object):
    def __init__(self, _id):
        self._id = _id

    def init(self):
        self.table = self.get_data(self._id)
        self.subject_column = self.get_subject_column(self._id)
        #self.classes = self.get_classes(self._id)
        #self.properties = self.get_properties(self._id)
        #self.entities = self.get_entities(self._id)

    def get_data(self, _id):
        return load_csv(os.path.join(TABLES_DIR, _id))

    def get_classes(self, _id):
        classes = []
        classes_list = load_csv(CLASSES_LIST)
        classes_list_filtered = classes_list[classes_list[:,0] == _id]
        for row in classes_list_filtered:
            if row[3] == '':
                headerRowIndices = [0]
            else:
                headerRowIndices = [ int(x) for x in row[3].split(".") ]
            _class = {
                "name": row[1],
                "uri": row[2],
                "headerRowIndices": headerRowIndices #dot separated values
            }
            classes.append(_class)
        return classes

    def get_properties(self, _id):
        properties = []
        properties_all = load_csv(os.path.join(PROPERTIES_DIR, _id))
        if properties_all == []:
            return []
        if properties_all.ndim > 1:
            for row in properties_all:
                _property = {
                    "uri": row[0],
                    "headerValue": row[1],
                    "isKey": False if row[2] == "False" else True,
                    "columnIndex": int(row[3])
                }
                properties.append(_property)
        else:
            row = properties_all
            _property = {
                "uri": row[0],
                "headerValue": row[1],
                "isKey": False if row[2] == "False" else True,
                "columnIndex": int(row[3])
            }
            properties.append(_property)
        return properties

    def get_subject_column(self, _id):
        csv = load_csv(SUBJECT_COLUMN_LIST)
        sc = csv[csv[:,0] == _id]
        if len(sc) > 0:
            return int(sc[0][1])
        else:
            return None

    def get_entities(self, _id):
        entities = []
        entities_list = load_csv(os.path.join(ENTITIES_DIR, _id))
        if entities_list == []:
            return []
        for row in entities_list:
            if len(row) > 2:
                continue
            entity = {
                "uri": row[0],
                "keyValue": row[1],
                "rowIndex": int(row[2])
            }
            entities.append(entity)
        return entities

    def is_subject_column(self, i):
        if i == self.subject_column:
            return True
        return False
