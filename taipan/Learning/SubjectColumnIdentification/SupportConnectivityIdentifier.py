from taipan.Logging.Logger import Logger
from taipan.Learning.SubjectColumnIdentification.SupportIdentifier import SupportIdentifier
from taipan.Learning.SubjectColumnIdentification.ConnectivityIdentifier import ConnectivityIdentifier

class SupportConnectivityIdentifier(object):
    def __init__(self):
        self.logger = Logger().getLogger(__name__)
        self.connectivityIdentifier = ConnectivityIdentifier()
        self.supportIdentifier = SupportIdentifier()

    def identifySubjectColumn(self, table, supportFloor=10, supportCeil=70, connectivityThreshold=0.01, alpha=0.5):
        connectivities = self.connectivityIdentifier.getConnectivity(table, applyWeights=False)
        supports = self.supportIdentifier.getSupport(table)

        supports = [support if support < supportCeil and support > supportFloor else 0 for support in supports]
        connectivities = [connectivity if connectivity > connectivityThreshold else 0 for connectivity in connectivities]

        #Make supports and connectivities on the same scale
        connectivities = [connectivity * 100 for connectivity in connectivities]
        #supports = [support / 10 for support in supports]

        consups = [0]*len(connectivities)
        for columnIndex, item in enumerate(consups):
            consups[columnIndex] = alpha*supports[columnIndex] + (1-alpha)*connectivities[columnIndex]

        return consups.index(max(consups))
