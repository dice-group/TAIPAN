import os
import codecs
from os import listdir
from os.path import isfile, join

tables_folder = "data/tables_aggregate"

tables_files = [f for f in listdir(tables_folder) if isfile(join(tables_folder, f))]

for _f in tables_files:
    print _f
    _f = os.path.join(tables_folder, _f)
    f = codecs.open(_f, "r", "utf-8")
    new_lines = []
    first_line_length = 0
    for num, line in enumerate(f.readlines()):
        if num == 0:
            first_line_length = len(line.split(","))
        line_length = len(line.split(","))
        if(line_length == first_line_length):
            new_lines.append(line)
    f.close()

    f = codecs.open(_f, "w", "utf-8")
    for line in new_lines:
        f.write(line)
    f.close()
