"""Generic Table"""

import uuid

class OsierTable(object):
    def __init__(self, table, _id=None):
        if _id:
            self._id = _id
        else:
            #random hash
            self._id = uuid.uuid4()

        self.table = table
        self.subject_column = 0

    def is_subject_column(self, i):
        if i == self.subject_column:
            return True
        return False

    def trim_table(self, number_of_rows=10):
        for num, col in enumerate(self.table):
            self.table[num] = col[:number_of_rows]
