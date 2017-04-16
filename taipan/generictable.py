"""Generic Table"""

import uuid

from taipan.util import load_csv

class GenericTable(object):
    def __init__(self, filename):
        self._id = uuid.uuid5(uuid.NAMESPACE_URL, "file://%s" % filename)
        self.filename = filename
        self.table = self.get_data(self.filename)
        self.subject_column = None

    def get_data(self, filename):
        return load_csv(filename)

    def is_subject_column(self, i):
        if i == self.subject_column:
            return True
        return False
