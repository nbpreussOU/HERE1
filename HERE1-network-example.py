import networkx as nx
from pylab import *

# helper function to load data in from file
def get_data(filename):
    with open(filename, 'r', encoding='utf-8') as rf:
        lines = rf.read().split("\n")
        data = [line.split(",") for line in lines]
        header = data[0]

        # remove header from data
        data = data[1:]

    return data


def calc_worst_waittime(flowin, patients, hours):
    right = 0
    wait = 0
    f = int(flowin)
    for j in range(f):
        right = right + (60 * j / patients)

    for k in range(hours):
        wait = wait + max(0, (flowin - patients) * 60 * k /patients * flowin) + right

    return wait


def calc_avg_waittime(flowin, patients, hours):
    right = 0
    wait = 0
    f = int(flowin)
    for j in range(f):
        right = right + max(0, (60/patients - 60/flowin) * j)

    for k in range(hours):
        wait = wait + max(0, (flowin - patients) * 60 * k / patients * flowin) + right

    return wait


# read in data from csv files
nodeData = get_data('HERE1-example-nodes.csv')
edgeData = get_data('HERE1-example-edges.csv')

# create the graph of the network
G = nx.DiGraph()

for node in nodeData:
    G.add_node(int(node[0]), name=node[1], patientsPerHour=int(node[2]))

for edge in edgeData:
    G.add_edge(int(edge[1]), int(edge[0]))

# CHANGE THIS VARIABLE TO CHANGE STARTING FLOW
startFlow = 10

# CHANGE THIS VARIABLE TO CHANGE WAITTIME CALCULATIONS
hour = 8

# Calculate various network flows
n1n2 = startFlow
G[1][2]['capacity'] = n1n2

node2In = n1n2
n2n4 = min(float(edgeData[1][3]), float(edgeData[1][2])*node2In/100)
G[2][4]['capacity'] = n2n4
n2n3 = min(float(edgeData[2][3]), float(edgeData[2][2])*node2In/100)
G[2][3]['capacity'] = n2n3

node3In = n2n3
n3n4 = min(float(edgeData[3][3]), float(edgeData[3][2])*node3In/100)
G[3][4]['capacity'] = n3n4

node4In = n2n4 + n3n4

# check to make sure that everything was implemented correctly
print("Data check on nodes and edges")
print(G.nodes.data())
print(G.edges.data())
print()

# analyze network flow
flow_value, flow_dict = nx.maximum_flow(G, 1, 4)
print("The maximum through the network is: ", flow_value)
print()

# calculating worst case wait times
wait2 = calc_worst_waittime(node2In, int(nodeData[1][2]), hour)
wait3 = calc_worst_waittime(node3In, int(nodeData[2][2]), hour)
wait4 = calc_worst_waittime(node4In, int(nodeData[3][2]), hour)
print("The worst case wait time for node 2 over the course of ", hour, " hours is: ", wait2, " minutes")
print("The worst case wait time for node 3 over the course of ", hour, " hours is: ", wait3, " minutes")
print("The worst case wait time for node 4 over the course of ", hour, " hours is: ", wait4, " minutes")

# calculating average case wait times
wait2a = calc_avg_waittime(node2In, int(nodeData[1][2]), hour)
wait3a = calc_avg_waittime(node3In, int(nodeData[2][2]), hour)
wait4a = calc_avg_waittime(node4In, int(nodeData[3][2]), hour)
print("The average case wait time for node 2 over the course of ", hour, " hours is: ", wait2a, " minutes")
print("The average case wait time for node 3 over the course of ", hour, " hours is: ", wait3a, " minutes")
print("The average case wait time for node 4 over the course of ", hour, " hours is: ", wait4a, " minutes")

# drawing the graph
nx.draw(G)
# TODO make the graph look prettier
show()
