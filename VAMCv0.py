import numpy as np
import networkx as nx
from pylab import *


# calculates the average case wait time at a given node, and returns the wait time of all patients at a given node
def calc_avg_wait_time(flowin, patients) -> int:
    wait = 0
    z = int(flowin)

    for j in range(z):
        wait = wait + max(0, (480 / patients - 480 / flowin) * j)

    return wait


# calculates the maximum wait time of a single patient at a given node
def calc_max_single_wait_time(flowin, patients) -> int:
    wait = max(0, (480 / patients - 480 / flowin) * flowin)

    return wait


# determines if there is a long wait time at a node, and sends latecomers home
def long_wait(flowin, patients) -> int:
    for k in range(int(flowin)):
        if max(0, (480 / patients - 480 / flowin) * k) > 30:
            return flowin - k

    return 0


class HCNetworkV0:
    def __init__(self):
        # randomize variables via poisson process
        # toned down the variance in the patient arrival distribution
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
        # define coordinates for the points
        pos_h = {
            0: [-1, 1],
            1: [-.4, .8],
            2: [.2, .6],
            3: [1.5, .2],
            4: [1, -.4],
            5: [.8, .4],
            6: [2.2, 0],
            7: [2.8, -.2]
        }

        figure(figsize=(12, 4), dpi=80)

        # raise the names for the nodes and edges above their respected points
        pos_attrs_e = {}
        for node, coords in pos_h.items():
            pos_attrs_e[node] = (coords[0], coords[1] + .07)

        pos_attrs_n = {}
        for node, coords in pos_h.items():
            pos_attrs_n[node] = (coords[0], coords[1] + .11)

        # add labels to the graph
        node_labels = nx.get_node_attributes(self.G, 'name')
        nx.draw_networkx_labels(self.G, pos_attrs_n, node_labels)
        edge_labels = nx.get_edge_attributes(self.G, 'capacity')
        nx.draw_networkx_edge_labels(self.G, pos_attrs_e, edge_labels)

        # change the arrow's thickness depending on the capacity
        thickness = []
        for node1, node2 in nx.get_edge_attributes(self.G, 'capacity'):
            weight = edge_labels[(node1, node2)]
            if weight == 0:
                thickness.append(.01)
            else:
                thickness.append(weight/20)

        nx.draw(self.G, pos_h, width=thickness, edge_color=thickness, edge_vmin=0, edge_vmax=5, edge_cmap=plt.cm.get_cmap('PiYG'))

        show()

    def get_data(self):
        # return edge data
        x = [self.nStartnCheckIn, self.nCheckInnNurse, self.nNursenPCP, self.nPCPnCheckOut, self.nNursenResident,
             self.nResidentnPCPEval, self.nPCPEvalnCheckOut, self.nCheckOutnEnd]
        return x

    def set_data(self, a, b, c, d, e, f, g, h):
        # create a network using any given edge data
        self.nStartnCheckIn = a
        self.nCheckInnNurse = b
        self.nNursenPCP = c
        self.nPCPnCheckOut = d
        self.nNursenResident = e
        self.nResidentnPCPEval = f
        self.nPCPEvalnCheckOut = g
        self.nCheckOutnEnd = h