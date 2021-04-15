import networkx as nx
from networkx.drawing.nx_agraph import to_agraph
from pylab import *

G = nx.DiGraph()
H = nx.DiGraph()

G.add_node(1, name="start")
G.add_node(2, name="receptionist")
G.add_node(3, name="paperwork")
G.add_node(4, name="end")

G.add_edge(1, 2)
G.add_edge(2, 3)
G.add_edge(3, 2)
G.add_edge(2, 4)

H.add_node(1, name="start")
H.add_node(2, name="receptionistA")
H.add_node(3, name="paperwork")
H.add_node(4, name="end")
H.add_node(5, name="receptionistB")

H.add_edge(1, 2)
H.add_edge(2, 3)
H.add_edge(3, 5)
H.add_edge(2, 4)
H.add_edge(5, 4)

# draw the graph
pos = nx.spring_layout(G)
nx.draw(G, pos)

pos_attrs = {}
for node, coords in pos.items():
    pos_attrs[node] = (coords[0], coords[1] + .08)

# add labels to the graph
node_labels = nx.get_node_attributes(G,'name')
nx.draw_networkx_labels(G, pos_attrs, node_labels)

show()

# draw the graph
pos = nx.spring_layout(H)
nx.draw(H, pos)

pos_attrs = {}
for node, coords in pos.items():
    pos_attrs[node] = (coords[0], coords[1] + .08)

# add labels to the graph
node_labels = nx.get_node_attributes(H,'name')
nx.draw_networkx_labels(H, pos_attrs, node_labels)

show()

