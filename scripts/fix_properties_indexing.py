import os
import codecs
from os import listdir
from os.path import isfile, join

properties_folder = "data/synthetic_dataset/properties"

properties_files = [f for f in listdir(properties_folder) if isfile(join(properties_folder, f))]

for _f in properties_files:
    print _f
    _f = os.path.join(properties_folder, _f)
    f = codecs.open(_f, "r", "utf-8")
    new_lines = []
    for line in f.readlines():
        if len(line) == 1:
            continue
        items = line.split(",")
        items[-1] = '"%s"\n' % (int(items[-1].replace('"', '').replace('\n','')) - 1,)
        new_lines.append(items)
    f.close()

    f = codecs.open(_f, "w", "utf-8")
    for line in new_lines:
        stringToWrite = u",".join(line)
        f.write(stringToWrite)
    f.close()
