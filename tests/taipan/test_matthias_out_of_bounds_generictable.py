"""Test for reported out of bound exception by Matthias W."""

from taipan.generictable import GenericTable
from taipan.ml.subjectcolumn.scidentifier import SCIdentifier

TABLE_STRING = """Verkaufsstellennr.;Name 1;Name 2;Name 3;Strasse;PLZ;Ort;Adresszusatz;Typ;Öffnungszeiten Montag 1;Öffnungszeiten Montag 2;Öffnungszeiten Montag 3;Öffnungszeiten Dienstag 1;Öffnungszeiten Dienstag 2;Öffnungszeiten Dienstag 3;Öffnungszeiten Mittwoch 1;Öffnungszeiten Mittwoch 2;Öffnungszeiten Mittwoch 3;Öffnungszeiten Donnerstag 1;Öffnungszeiten Donnerstag 2;Öffnungszeiten Donnerstag 3;Öffnungszeiten Freitag 1;Öffnungszeiten Freitag 2;Öffnungszeiten Freitag 3;Öffnungszeiten Samstag 1;Öffnungszeiten Samstag 2;Öffnungszeiten Samstag 3;Öffnungszeiten Sonntag 1;Öffnungszeiten Sonntag 2;Öffnungszeiten Sonntag 3;Koord_Lat;Koord_Lon
503979;Reisezentrum Aachen Hbf;;;Bahnhofplatz 2a;52064;Aachen;;Reisezentrum;06:00-21:00;;;06:00-21:00;;;06:00-21:00;;;06:00-21:00;;;06:00-21:00;;;07:00-20:00;;;08:00-20:00;;;50768944;6090200"""

def test():
    table = GenericTable("stub", csv_string=TABLE_STRING, delimiter=";")
    table.init()
    sc_ident = SCIdentifier()
    subject_column = sc_ident.identify_subject_column(table)
    assert subject_column == [4, 6]
