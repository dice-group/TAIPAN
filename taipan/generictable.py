"""Generic Table"""

import uuid

from taipan.util import load_csv_commas

class GenericTable(object):
    def __init__(self, filename, _id=None):
        if _id:
            self._id = _id
        else:
            self._id = uuid.uuid5(uuid.NAMESPACE_URL, "file://%s" % filename)

        self.filename = filename

    def init(self):
        self.table = self.get_data(self.filename)
        self.subject_column = None

    def get_data(self, filename):
        return load_csv_commas(filename)

    def is_subject_column(self, i):
        if i == self.subject_column:
            return True
        return False

    def trim_table(self, number_of_rows=10):
        for num, col in enumerate(self.table):
            self.table[num] = col[:number_of_rows]
