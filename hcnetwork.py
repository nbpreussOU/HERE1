import numpy as np
import networkx as nx
from pylab import *


def calc_avg_wait_time(flowin, patients) -> int:
    wait = 0
    f = int(flowin)

    for j in range(f):
        wait = wait + max(0, (480 / patients - 480 / flowin) * j)

    return wait


def calc_max_single_wait_time(flowin, patients) -> int:
    wait = max(0, (480 / patients - 480 / flowin) * flowin)

    return wait


class HCNetwork:
    def __init__(self):
        # randomize variables via poisson process
        self.pStart = np.random.poisson(50, 1)[0].item()
        self.pCheckIn = np.random.poisson(64, 1)[0].item()
        self.pNurse = np.random.poisson(192, 1)[0].item()
        self.pPCPEval = np.random.poisson(160, 1)[0].item()
        self.pPCP = np.random.poisson(16, 1)[0].item()
        self.pResident = np.random.poisson(40, 1)[0].item()
        self.pCheckOut = np.random.poisson(64, 1)[0].item()

        self.multi = np.random.multinomial(100, [1/7.]*5 + [2/7.])

        # calculate capacity of the edges
        self.nStartnCheckIn = self.pStart
        self.nCheckInnNurse = min(self.nStartnCheckIn, self.pCheckIn)
        self.nNursenBranch = min(self.nCheckInnNurse, self.pNurse)

        self.multi = np.random.multinomial(self.nNursenBranch, [76/100., 24/100.])
        self.nNursenResident = self.multi[0].item()
        self.nNursenPCP = self.multi[1].item()

        self.nResidentnPCPEval = min(self.nNursenResident, self.pResident)
        self.nPCPEvalnCheckOut = min(self.nResidentnPCPEval, self.pPCPEval)
        self.nPCPnCheckOut = min(self.nNursenPCP, self.pPCP)
        self.nCheckOutnEnd = min(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)

        # initialize the graph
        self.G = nx.DiGraph()

    def build_network(self):

        # create the nodes
        self.G.add_nodes_from([
            (0, {"name": "start"}),
            (1, {"name": "Check In"}),
            (2, {"name": "Nurse"}),
            (3, {"name": "PCP Evaluation"}),
            (4, {"name": "PCP"}),
            (5, {"name": "Resident"}),
            (6, {"name": "Check Out"}),
            (7, {"name": "End"}),
        ])

        # create the edges
        self.G.add_edges_from([(0, 1), (1, 2), (2, 4), (4, 6), (2, 5), (5, 3), (3, 6), (6, 7)])

        # add the capacity to the edges in patients per day
        self.G[0][1]['capacity'] = self.nStartnCheckIn
        self.G[1][2]['capacity'] = self.nCheckInnNurse
        self.G[2][4]['capacity'] = self.nNursenPCP
        self.G[4][6]['capacity'] = self.nPCPnCheckOut
        self.G[2][5]['capacity'] = self.nNursenResident
        self.G[5][3]['capacity'] = self.nResidentnPCPEval
        self.G[3][6]['capacity'] = self.nPCPEvalnCheckOut
        self.G[6][7]['capacity'] = self.nCheckOutnEnd

        # add the wait time to the edges as weight
        self.G[0][1]['weight'] = calc_max_single_wait_time(self.nStartnCheckIn, self.pCheckIn)
        self.G[1][2]['weight'] = calc_max_single_wait_time(self.nCheckInnNurse, self.pNurse)
        self.G[2][4]['weight'] = calc_max_single_wait_time(self.nNursenPCP, self.pPCP)
        self.G[4][6]['weight'] = calc_max_single_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        self.G[2][5]['weight'] = calc_max_single_wait_time(self.nNursenResident, self.pResident)
        self.G[5][3]['weight'] = calc_max_single_wait_time(self.nResidentnPCPEval, self.pPCPEval)
        self.G[3][6]['weight'] = calc_max_single_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        self.G[6][7]['weight'] = 0

    def analyze_network(self):
        # calculate maximum flow
        flow_value, flow_dict = nx.maximum_flow(self.G, 0, 7)

        # calculate maximum single person wait time
        bottom_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][4]['weight'] + self.G[4][6]['weight'] + self.G[6][7]['weight']
        top_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][5]['weight'] + self.G[5][3]['weight'] + self.G[3][6]['weight'] + self.G[6][7]['weight']
        longest_wait = max(bottom_path, top_path)

        # calculate efficiency
        efficiency = flow_value / self.pStart * 100

        # calculate total wait time
        a = calc_avg_wait_time(self.nStartnCheckIn, self.pCheckIn)
        b = calc_avg_wait_time(self.nCheckInnNurse, self.pNurse)
        c = calc_avg_wait_time(self.nNursenPCP, self.pPCP)
        d = calc_avg_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        e = calc_avg_wait_time(self.nNursenResident, self.pResident)
        f = calc_avg_wait_time(self.nResidentnPCPEval, self.pPCPEval)
        total_wait = a + b + c + d + e + f

        return_vals = [self.pStart, flow_value, efficiency, longest_wait, total_wait]

        return return_vals

    def visualize_network(self):
        # draw the graph
        pos = nx.spring_layout(self.G)
        nx.draw(self.G, pos)

        pos_attrs = {}
        for node, coords in pos.items():
            pos_attrs[node] = (coords[0], coords[1] + .08)

        # add labels to the graph
        node_labels = nx.get_node_attributes(self.G, 'name')
        nx.draw_networkx_labels(self.G, pos_attrs, node_labels)
        edge_labels = nx.get_edge_attributes(self.G, 'capacity')
        nx.draw_networkx_edge_labels(self.G, pos_attrs, edge_labels)

        show()
