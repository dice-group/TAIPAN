"""Tests for GenericTable"""

import os

from taipan.pathes import TABLES_DIR
from taipan.generictable import GenericTable

TEST_FILENAME = os.path.join(TABLES_DIR, "000ec48b-f25f-47ef-af12-1f897207cdb4.csv")

def test_init():
    table = GenericTable(TEST_FILENAME)
    table.init()
    assert len(table.table) == 13
    assert table.subject_column is None
