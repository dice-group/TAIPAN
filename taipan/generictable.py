"""Generic Table"""

import uuid

from taipan.csvloader import CSVLoader

class GenericTable(object):
    def __init__(self, filename=None, _id=None, csv_string=None):
        if _id:
            self._id = _id
        else:
            self._id = uuid.uuid5(uuid.NAMESPACE_URL, "file://%s" % filename)

        if filename:
            self.filename = filename
        if csv_string:
            self.csv_string = csv_string

        self.csv_loader = CSVLoader()

    def init(self):
        if hasattr(self, 'csv_string') and self.csv_string:
            self.table = self.get_data(self.csv_string)
        else:
            _f = open(self.filename)
            self.table = self.get_data(_f)
        self.subject_column = None

    def get_data(self, _csv):
        return self.csv_loader.load_csv(_csv)

    def is_subject_column(self, i):
        if i == self.subject_column:
            return True
        return False

    def trim_table(self, number_of_rows=10):
        for num, col in enumerate(self.table):
            self.table[num] = col[:number_of_rows]
