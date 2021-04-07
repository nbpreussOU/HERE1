import VAMCv0
import numpy as np
import networkx as nx


class HCNetworkV2(VAMCv0.HCNetworkV0):
    def __init__(self):
        super().__init__()

    def initialize(self):
        # randomize variables via poisson process
        self.pStart = int(np.random.normal(50, 4))
        self.pCheckIn = int(np.random.normal(64, 4))
        self.pNurse = int(np.random.normal(192, 4))
        self.pPCPEval = int(np.random.normal(160, 4))
        self.pPCP = int(np.random.normal(16, 3))
        self.pResident = int(np.random.normal(40, 4))
        self.pCheckOut = int(np.random.normal(50, 4))

        # calculate capacity of the edges
        self.nStartnCheckIn = self.pStart
        self.nCheckInnNurse = min(self.nStartnCheckIn, self.pCheckIn)
        self.nNursenBranch = min(self.nCheckInnNurse, self.pNurse)

        self.multi = np.random.multinomial(self.nNursenBranch, [76 / 100., 24 / 100.])
        self.nNursenResident = self.multi[0].item()
        self.nNursenPCP = self.multi[1].item()

        self.nResidentnPCPEval = min(self.nNursenResident, self.pResident)
        self.nPCPEvalnCheckOut = min(self.nResidentnPCPEval, self.pPCPEval)

        self.nPCPnCheckOut = min(self.nNursenPCP, self.pPCP)
        self.nCheckOutnEnd = min(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)

        # initialize the graph
        self.G = nx.DiGraph()
