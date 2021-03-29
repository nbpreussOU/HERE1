import VAMCv0


class HCNetworkV1(VAMCv0.HCNetworkV0):
    def __init__(self):
        # use the parent method to initialize most of the variables
        super().__init__()

        # update variables for new topology
        self.nPCPnEnd = VAMCv0.long_wait(self.nNursenPCP, self.pPCP)
        self.nPCPnCheckOut = min(self.nNursenPCP - self.nPCPnEnd, self.pPCP)
        self.nCheckOutnEnd = min(self.nPCPnCheckOut + self.nPCPEvalnCheckOut, self.pCheckOut)

    def build_network(self):
        # create the edges
        super().build_network()

        # add new edges from the topology
        self.G.add_edges_from([(4, 7)])
        self.G[4][7]['capacity'] = self.nPCPnEnd
        self.G[4][7]['weight'] = 0

    def get_data(self):
        # return edge data
        x = super().get_data()
        x.append(self.nPCPnEnd)
        return x

    def set_data(self, a, b, c, d, e, f, g, h, i):
        # create a network using any given edge data
        super().set_data(a, b, c, d, e, f, g, h)
        self.nPCPnEnd = i
