import networkx as nx
from pylab import *


# calculates the average case wait time at a given node, and returns the wait time of all patients at a given node
def calc_avg_wait_time(flowin, patients) -> int:
    """Calculates wait time in the average case

    Parameters
    ----------

    flow in : Int
        The number of patients per time frame that flow in to a given node
    patients : Int
        The number of patients per time frame that a node can process

    Returns
    ----------
    int
        the total wait time experienced at a node in the average case
    """
    if patients <= 0:
        patients = 1

    if flowin <= 0:
        flowin = 1

    wait = 0
    z = int(flowin)

    # range(z) gives integers of 0, 1, 2, ... , z-2, z-1
    for j in range(z):
        wait = wait + max(0, (480 / patients - 480 / flowin) * j)

    return wait


# calculates the maximum wait time of a single patient at a given node
def calc_max_single_wait_time(flowin, patients) -> int:
    """Calculates the maximum time a single patient will have to wait at the node

    Parameters
    ----------

    flow in : Int
        The number of patients per time frame that flow in to a given node
    patients : Int
        The number of patients per time frame that a node can process

    Returns
    ----------
    int
        the longest wait time experienced by a patient at a node
    """
    if patients <= 0:
        patients = 1

    if flowin <= 0:
        flowin = 1

    wait = max(0, (480 / patients - 480 / flowin) * (flowin - 1))

    return wait


# determines if there is a long wait time at a node, and sends latecomers home
def long_wait(flowin, patients) -> int:
    """Removes patients from a node if the wait time exceeds a certain value

    Parameters
    ----------

    flow in : Int
        The number of patients per time frame that flow in to a given node
    patients : Int
        The number of patients per time frame that a node can process

    Returns
    ----------
    int
        the number of patients turned away by long wait time
    """
    if patients <= 0:
        patients = 1

    if flowin <= 0:
        flowin = 1

    for k in range(int(flowin)):
        if max(0, (480 / patients - 480 / flowin) * k) > 30:
            return flowin - k

    return 0


class HCNetworkV0:
    """
    A class that houses a healthcare network flow model

    Uses networkx to build the network model, and pylab
    from matplotlib to draw it

    Methods
    -------

    initialize()
        Assigns nodes their random values and calculates the edge's capacity
    build_network():
        Creates the network as a networkx graph
    analyze_network(): List
        Calculates the metrics used to evaluate the network and returns them as a list
    visualize_network():
        Modifies attributes of the network and then displays the network
    get_data(): List
        returns a list of all the edge capacities
    set_data(data):
        sets the edge capacities to values contined in the list data
    """
    def __init__(self):
        """Initializes all variables used in the model, but does not set them to a relevant value"""
        # all variables randomized at a later point in time, but the variables needed to be instantiated so...
        self.pStart = 1
        self.pCheckIn = 1
        self.pNurse = 1
        self.pPCPEval = 1
        self.pPCP = 1
        self.pResident = 1
        self.pCheckOut = 1
        self.multi = 1
        self.nStartnCheckIn = 1
        self.nCheckInnNurse = 1
        self.nNursenBranch = 1
        self.multi = 1
        self.nNursenResident = 1
        self.nNursenPCP = 1
        self.nResidentnPCPEval = 1
        self.nPCPEvalnCheckOut = 1
        self.nPCPnCheckOut = 1
        self.nCheckOutnEnd = 1
        self.G = 1

    def initialize(self):
        """Randomizes values for the nodes and calculates edge capacity"""
        # randomize variables via poisson process
        self.pStart = np.random.poisson(50, 1)[0].item()
        self.pCheckIn = np.random.poisson(64, 1)[0].item()
        self.pNurse = np.random.poisson(192, 1)[0].item()
        self.pPCPEval = np.random.poisson(160, 1)[0].item()
        self.pPCP = np.random.poisson(16, 1)[0].item()
        self.pResident = np.random.poisson(40, 1)[0].item()
        self.pCheckOut = np.random.poisson(64, 1)[0].item()

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

    def build_network(self):
        """Creates the network in networkx and assigns capacities and weights to the edges of the graph"""
        # create the nodes
        self.G.add_nodes_from([
            (0, {"name": "Start"}),
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
        a = calc_avg_wait_time(self.nStartnCheckIn, self.pCheckIn)
        b = calc_avg_wait_time(self.nCheckInnNurse, self.pNurse)
        c = calc_avg_wait_time(self.nNursenPCP, self.pPCP)
        d = calc_avg_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        e = calc_avg_wait_time(self.nNursenResident, self.pResident)
        f = calc_avg_wait_time(self.nResidentnPCPEval, self.pPCPEval)
        total_wait = a + b + c + d + e + f

        # round values to make them presentable
        flow_value = round(flow_value, 3)
        efficiency = round(efficiency, 3)
        longest_wait = round(longest_wait, 3)
        total_wait = round(total_wait)

        return_vals = [self.pStart, flow_value, efficiency, longest_wait, total_wait]

        return return_vals

    def visualize_network(self, filename):
        """Modifies attributes of the graph and then visualize the graph"""
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

        figure(figsize=(14, 4), dpi=80)

        plt.xlim(-1.5, 3.3)
        plt.ylim(-.5, 1.2)

        # raise the names for the nodes and edges above their respected points
        pos_attrs_e = {}
        for node, coords in pos_h.items():
            pos_attrs_e[node] = (coords[0], coords[1] - .08)

        pos_attrs_n = {}
        for node, coords in pos_h.items():
            pos_attrs_n[node] = (coords[0], coords[1] + .13)

        # add labels to the graph
        node_labels = nx.get_node_attributes(self.G, 'name')
        nx.draw_networkx_labels(self.G, pos_attrs_n, node_labels, font_size=14)
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

        # grab images
        name = "Images/" + filename + ".png"
        savefig(name)
        show()

    def get_data(self):
        """Returns the capacities of the edges of the graph

        Returns
        ----------
        list
            list of the capacities in the edges of the graphs
        """
        # return edge data
        x = [self.nStartnCheckIn, self.nCheckInnNurse, self.nNursenPCP, self.nPCPnCheckOut, self.nNursenResident,
             self.nResidentnPCPEval, self.nPCPEvalnCheckOut, self.nCheckOutnEnd]
        return x

    def set_data(self, data):
        """Assigns the capacities in a list of data to the edges of the graph

        Parameters
        ----------
        data:list
            list of the capacities in the edges of the graphs
        """
        # create a network using any given edge data
        self.nStartnCheckIn = data[0]
        self.nCheckInnNurse = data[1]
        self.nNursenPCP = data[2]
        self.nPCPnCheckOut = data[3]
        self.nNursenResident = data[4]
        self.nResidentnPCPEval = data[5]
        self.nPCPEvalnCheckOut = data[6]
        self.nCheckOutnEnd = data[7]
