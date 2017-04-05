"""Utils"""
import numpy
import os
import re

def load_csv(csvPath):
    """Load CSV file to numpy array"""
    if(os.path.exists(csvPath) and os.stat(csvPath).st_size):
        csv_bytes = numpy.genfromtxt(
            csvPath,
            delimiter=",",
            dtype="S",
            comments="///",
            missing_values="NULL",
            invalid_raise=False
        )
        csv = csv_bytes.view(numpy.chararray).decode("utf-8")
        if numpy.shape(csv) != (0,):
            for x in numpy.nditer(csv, op_flags=['readwrite']):
                x[...] = x.flatten()[0].strip('"')
            return csv
        else:
            return []
    else:
        return []

def clear_string(string):
    string = re.sub('[{}|*?()\[\]!-"]', '', string)
    string = re.sub('&nbsp;', '', string)
    string = string.strip()
    return string
