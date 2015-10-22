import os
import os.path
from numpy import genfromtxt
import matplotlib.pyplot as plt


class DistantSupervisionAnalyzer(object):
    packageDirectory = os.path.dirname(os.path.abspath(__file__))
    resultsDirectory = os.path.join(packageDirectory, "../../../results/dlsi/0-100_10")

    def __init__(self):
        pass

    def parseResultsCsv(self, filename):
        filepath = os.path.join(self.resultsDirectory, filename)
        csv = genfromtxt(filepath, delimiter=",", dtype="S", comments="///", missing_values="NULL")
        header = csv[0]
        data = csv[1:]
        precision = 0
        for row in data:
            if row[4] == 'True':
                precision += 1
        precision = float(precision) / len(data)
        return precision

    def getResult(self, support, connectivity):
        baseFilename = "rows_%s.support_%s.connectivity_%s.hot.csv." % (str(20), str(support), str(connectivity),)
        run = 1
        filename = baseFilename + str(run)
        precision = self.parseResultsCsv(filename)
        return (precision, connectivity, support)
        #return {"support": support, "connectivity": connectivity, "precision": precision}

    def getResults(self):
        __precision = []
        __connectivity = []
        __support = []
        for support in range(0, 100, 10):
            for connectivity in range(0, 100, 10):
                (_precision, _connectivity, _support) = self.getResult(support, connectivity)
                __precision.append(_precision)
                __connectivity.append(_connectivity)
                __support.append(_support)
        return (__precision, __connectivity, __support)

    def plotResults(self):
        (precision, connectivity, support) = self.getResults()
        _precision = []
        _connectivity = []
        _support = []
        plt.figure(1)
        for i in range(0, 10):
            pr = precision[i*10:i*10+10]
            cn = connectivity[i*10:i*10+10]
            splbl = support[i*10:i*10+10]
            splbl = splbl[0]
            plt.subplot(10,1,i+1)
            plt.xlabel('Connectivity')
            plt.ylabel('Precision')
            plt.title('Support %s' % (splbl,))
            plt.grid(True)
            plt.plot(cn, pr, 'b-')

        plt.show()

if __name__ == "__main__":
    dsa = DistantSupervisionAnalyzer()
    dsa.plotResults()
