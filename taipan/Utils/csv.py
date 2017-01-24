import numpy
import os

def loadCsv(csvPath):
    if(os.path.exists(csvPath)):
        csv_bytes = numpy.genfromtxt(csvPath, delimiter=",", dtype="S", comments="///", missing_values="NULL")
        csv = csv_bytes.view(numpy.chararray).decode("utf-8")
        if numpy.shape(csv) != (0,):
            for x in numpy.nditer(csv, op_flags=['readwrite']):
                x[...] = x.flatten()[0].strip('"')
            return csv
        else:
            return []
    else:
        return []
