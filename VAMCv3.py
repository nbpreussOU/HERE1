import VAMCv0
import numpy as np
import networkx as nx
import math


class HCNetworkV3(VAMCv0.HCNetworkV0):
    def __init__(self):
        super().__init__()

    def initialize(self, i):
        # randomize variables via poisson process
        self.pStart = max(1, int(np.random.normal(50, math.sqrt(50) / 10 * i)))
        self.pCheckIn = max(1, int(np.random.normal(64, math.sqrt(64) / 10 * i)))
        self.pNurse = max(1, int(np.random.normal(192, math.sqrt(192) / 10 * i)))
        self.pPCPEval = max(1, int(np.random.normal(160, math.sqrt(160) / 10 * i)))
        self.pPCP = max(1, int(np.random.normal(16, math.sqrt(16) / 10 * i)))
        self.pResident = max(1, int(np.random.normal(40, math.sqrt(40) / 10 * i)))
        self.pCheckOut = max(1, int(np.random.normal(50, math.sqrt(50) / 10 * i)))

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

    def analyze_network(self, i):
        """Analyzes the networks according to various metrics

        Returns
        ----------
        list
            a list contianing the flow in, flow out, efficiency, the longest wait time, and the total wait time
        """
        # calculate maximum flow
        flow_value, flow_dict = nx.maximum_flow(self.G, 0, 7)

        # calculate maximum single person wait time
        bottom_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][4]['weight'] + self.G[4][6]['weight'] + self.G[6][7]['weight']
        top_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][5]['weight'] + self.G[5][3]['weight'] + self.G[3][6]['weight'] + self.G[6][7]['weight']
        longest_wait = max(bottom_path, top_path)

        # calculate efficiency
        efficiency = flow_value / self.pStart * 100

        # calculate total wait time
        a = VAMCv0.calc_avg_wait_time(self.nStartnCheckIn, self.pCheckIn)
        b = VAMCv0.calc_avg_wait_time(self.nCheckInnNurse, self.pNurse)
        c = VAMCv0.calc_avg_wait_time(self.nNursenPCP, self.pPCP)
        d = VAMCv0.calc_avg_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        e = VAMCv0.calc_avg_wait_time(self.nNursenResident, self.pResident)
        f = VAMCv0.calc_avg_wait_time(self.nResidentnPCPEval, self.pPCPEval)
        total_wait = a + b + c + d + e + f

        # round values to make them presentable
        flow_value = round(flow_value, 3)
        efficiency = round(efficiency, 3)
        longest_wait = round(longest_wait, 3)
        total_wait = round(total_wait)

        return_vals = [i, self.pStart, flow_value, efficiency, longest_wait, total_wait]

        return return_vals
