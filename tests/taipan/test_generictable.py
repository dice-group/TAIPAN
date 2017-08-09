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

TABLE_STRING = '"Region","Currency","Price","Price in ?"\n"Australia SA+WA","AUD","24.95","15.91"\n"Israel","ILS","79","15.03"\n"Australia","AUD","19.99","12.75"\n"Kuwait","KWD","4.50","11.08"\n"Canada","CAD","14.99","10.02"\n"GreeceFinland","EUR","9.95","9.95"\n"Czech","CZK","249","9.55"\n"Turkey","TRY","19.95","9.48"\n"Romania","RON","39","9.34"\n"Hungary","HUF","2490","9.19"\n"Hong Kong","HKD","99.9","9.09"\n"Singapore","SGD","17.90","9.02"\n"Malaysia","MYR","39.90","8.31"\n"Russia","RUR","349","8.27"\n"Japan","JPY","999","7.87"\n"Poland","PLN","29.99","7.34"\n"China","CNY","69.00","7.15"\n"Switzerland","CHF","9.95","6.76"\n"Ireland","EUR","4.90","4.90"\n"United Kingdom","GBP","4.99","5.69"\n"United States","USD","7.99","5.65"\n"Denmark","DKK","39","5.24"\n"Portugal","EUR","5.03","5.03"\n"AustriaBelgiumGermanyItalyNetherlandsSlovakiaSpain","EUR","4.99","4.99"\n"France","EUR","4.95","4.95"\n"Ikealand","SEK","49","4.77"\n"Norway","NOK","39","4.73 cheapest!"\n'

def test_from_string():
    table = GenericTable("stub", csv_string=TABLE_STRING)
    table.init()
    assert len(table.table) == 28
    assert table.subject_column is None
