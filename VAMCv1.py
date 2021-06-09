import networkx as nx

import VAMCv0


class HCNetworkV1(VAMCv0.HCNetworkV0):
    """
        A class that houses a healthcare network flow model

        Uses networkx to build the network model, and pylab
        from matplotlib to draw it

        Extends the base model class to reduce rewriting of code

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
        """Calls the parent function, then initializes all new
        variables used in the model, but does not set them to a relevant value"""
        # use the parent method to initialize most of the variables
        super().__init__()
        self.nPCPnEnd = 1
        self.nPCPnCheckOut = 1
        self.nCheckOutnEnd = 1

    def initialize(self):
        """Calls the parent function, then randomizes the new variables"""
        super().initialize()
        # update variables for new topology
        self.nPCPnEnd = VAMCv0.long_wait(self.nNursenPCP, self.pPCP)
        self.nPCPnCheckOut = min(self.nNursenPCP - self.nPCPnEnd, self.pPCP)
        self.nCheckOutnEnd = min(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)

    def build_network(self):
        """Calls the parent function, then modifies the model to account for the new topology"""
        # create the edges
        super().build_network()

        # add new edges from the topology and change necessary weights to account for patients removed from system
        self.G.add_edges_from([(4, 7)])
        self.G[4][7]['capacity'] = self.nPCPnEnd
        self.G[4][7]['weight'] = 0
        self.G[2][4]['weight'] = VAMCv0.calc_max_single_wait_time(self.nNursenPCP-self.nPCPnEnd, self.pPCP)

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
        bottom_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][4]['weight'] + self.G[4][6][
            'weight'] + self.G[6][7]['weight']
        top_path = self.G[0][1]['weight'] + self.G[1][2]['weight'] + self.G[2][5]['weight'] + self.G[5][3]['weight'] + \
                   self.G[3][6]['weight'] + self.G[6][7]['weight']
        longest_wait = max(bottom_path, top_path)

        # calculate efficiency
        efficiency = flow_value / self.pStart * 100

        # calculate total wait time
        a = VAMCv0.calc_avg_wait_time(self.nStartnCheckIn, self.pCheckIn)
        b = VAMCv0.calc_avg_wait_time(self.nCheckInnNurse, self.pNurse)
        # people are sent straight home, so they don't count towards wait time ehehe
        c = VAMCv0.calc_avg_wait_time(self.nNursenPCP - self.nPCPnEnd, self.pPCP)
        d = VAMCv0.calc_avg_wait_time(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)
        e = VAMCv0.calc_avg_wait_time(self.nNursenResident, self.pResident)
        f = VAMCv0.calc_avg_wait_time(self.nResidentnPCPEval, self.pPCPEval)
        total_wait = a + b + c + d + e + f

        # round values to make them presentable
        flow_value = round(flow_value, 3)
        efficiency = round(efficiency, 3)
        longest_wait = round(longest_wait, 3)
        total_wait = round(total_wait)

        return_vals = [self.pStart, flow_value, efficiency, longest_wait, total_wait]

        return return_vals

    def get_data(self):
        """Returns the capacities of the edges of the graph

        Returns
        ----------
        list
           list of the capacities in the edges of the graphs
        """
        # return edge data
        x = super().get_data()
        x.append(self.nPCPnEnd)
        return x

    def set_data(self, data):
        """Assigns the capacities in a list of data to the edges of the graph

        Parameters
        ----------
        data:list
            list of the capacities in the edges of the graphs
        """
        # create a network using any given edge data
        super().set_data(data)
        self.nPCPnEnd = data[8]
