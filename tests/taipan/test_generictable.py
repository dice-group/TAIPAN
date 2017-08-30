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

tomtom_csv = """timestamp longitude latitude "speed m/s"
1305093212000 13.587170 52.425710 8.33
1305093213000 13.587030 52.425690 8.33
1305093214000 13.586920 52.425690 8.33
1305093215000 13.586810 52.425660 8.33
1305093216000 13.586730 52.425650 3.89
1305093217000 13.586680 52.425650 3.89
1305093218000 13.586620 52.425640 3.89
1305093219000 13.586580 52.425630 3.89
1305093220000 13.586530 52.425630 3.89
1305093221000 13.586470 52.425630 3.89
1305093222000 13.586370 52.425600 3.89
1305093223000 13.586310 52.425590 3.89
1305093224000 13.586250 52.425580 3.89
1305093225000 13.586200 52.425580 3.89
1305093226000 13.586140 52.425570 3.89
1305093227000 13.586090 52.425640 12.50
1305093228000 13.586040 52.425740 12.50"""

def test_space_delimiter():
    table = GenericTable("stub", csv_string=tomtom_csv, delimiter=" ")
    table.init()
    assert table.table.shape == (18, 4)
    assert table.subject_column is None
