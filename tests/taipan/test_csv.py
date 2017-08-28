"""Test CSV parsing."""

from csv import reader, list_dialects, \
    Dialect, QUOTE_MINIMAL, register_dialect

class GermanCSV(Dialect):
    delimiter=','
    quotechar = '"'
    doublequote = False
    skipinitialspace = True
    lineterminator = '\n'
    quoting = QUOTE_MINIMAL
register_dialect("GermanCSV", GermanCSV)

def check_csv(_iterable, _dialect):
    _r = reader(_iterable, dialect=_dialect)
    header_length = 0
    for num, line in enumerate(_r):
        if num == 0:
            header_length = len(line)
        assert len(line) > 2
        assert len(line) == header_length

check_csv(open("test_csv_1.csv"), "GermanCSV")

german_csv_line = """STRECKE_NR,RICHTUNG,KM_I,KM_L,BEZEICHNUNG,TECHN_SICHERUNG,STRASSENART,GEOGR_BREITE,GEOGR_LAENGE,GK_H_DGN,GK_R_DGN
1000,0,117310013,"173,1 + 13",Bü 173.114 Flensburg-Weiche - Flensb. Gr,Schrankenabschluss,Strasse,54.759941,9.39961214,6070137.808,3525801.083
1000,0,117730060,"177,3 + 60",Bü 177.36 Flensburg-Weiche - Flensb. Gr,Schrankenabschluss,Strasse,54.79452802,9.37456587,6073979.067,3524168.173
1000,0,117840036,"178,4 + 36",Bü 178.436 Flensburg-Weiche - Flensb. Gr,Schrankenabschluss,Strasse,54.80371842,9.36938291,6075000.359,3523829.416
1000,0,117910013,"179,1 + 13",Bü 179.113 Flensburg-Weiche - Flensb. Gr,Nicht technisch gesichert,Strasse,54.80950055,9.36611999,6075642.917,3523616.232
1000,0,117950053,"179,5 + 53",Bü 179.552 Flensburg-Weiche - Flensb. Gr,Nicht technisch gesichert,Strasse,54.81325834,9.36399819,6076060.519,3523477.636
"""

import io

check_csv(io.StringIO(german_csv_line), "GermanCSV")

class GermanCSVSemicolon(Dialect):
    delimiter=';'
    quotechar = '"'
    doublequote = False
    skipinitialspace = True
    lineterminator = '\n'
    quoting = QUOTE_MINIMAL
register_dialect("GermanCSVSemicolon", GermanCSVSemicolon)

check_csv(open("test_csv_2.csv"), "GermanCSVSemicolon")

german_csv_line = """Bundesland;RB;BM;Bf. Nr.;Station;"Bf DS 100 Abk.";"Kat. Vst";Straße;PLZ;Ort;Aufgabenträger
Hessen;RB Mitte;Darmstadt;119;Altheim (Hess);FAT;6;Münstererstr. 19;64839;Münster;Rhein-Main-Verkehrsverbund GmbH
Hessen;RB Mitte;Darmstadt;201;Assmannshausen;FAH;5;Bahnhofstr. 1;65385;Rüdesheim am Rhein;Rhein-Main-Verkehrsverbund GmbH
Hessen;RB Mitte;Darmstadt;230;Auringen-Medenbach;FAM;6;August-Ruf-Straße 50;65207;Wiesbaden;Rhein-Main-Verkehrsverbund GmbH
Hessen;RB Mitte;Darmstadt;238;Babenhausen (Hess);FBA;5;Am Bahnhof 1;64832;Babenhausen;Rhein-Main-Verkehrsverbund GmbH
Hessen;RB Mitte;Darmstadt;3564;Babenhausen Langstadt;FLAS;7;Kleestädter-Str. 75;64832;Babenhausen;Rhein-Main-Verkehrsverbund GmbH
Hessen;RB Mitte;Darmstadt;292;Bad König;FKI;6;Bahnhofsplatz 1;64732;Bad König;Rhein-Main-Verkehrsverbund GmbH
"""

check_csv(io.StringIO(german_csv_line), "GermanCSVSemicolon")
