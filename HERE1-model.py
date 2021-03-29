import VAMCv0 as v0
import VAMCv1 as v1
import pandas as pd

# create a list to store all our values
v0_data = []
v0_mega_network = []
v1_data = []
v1_mega_network = []

# create 100 different networks and store the results
for a in range(0, 100):
    # build original network
    x = v0.HCNetworkV0()
    x.build_network()
    v0_data.append(x.analyze_network())
    v0_mega_network.append(x.get_data())

    #build network with topology changes
    y = v1.HCNetworkV1()
    y.build_network()
    v1_data.append(y.analyze_network())
    v1_mega_network.append(y.get_data())


# create a dataframe from the values we got and write it out to a csv
df = pd.DataFrame(v0_data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
df.to_csv(r'v0_data.csv', index=False)

df = pd.DataFrame(v1_data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
df.to_csv(r'v1_data.csv', index=False)


# create mega network for topology version 0
df2 = pd.DataFrame(v0_mega_network)
v0_total_network = df2.sum()
v0_percentage_network = [float(i) for i in v0_total_network]

flow_in = v0_percentage_network[0]

for i in range(len(v0_percentage_network)):
    v0_percentage_network[i] = round(v0_percentage_network[i] / flow_in * 100, 2)

# build the network and visualize it
percent = v0.HCNetworkV0()
percent.set_data(v0_percentage_network[0], v0_percentage_network[1], v0_percentage_network[2], v0_percentage_network[3], v0_percentage_network[4], v0_percentage_network[5], v0_percentage_network[6], v0_percentage_network[7])
percent.build_network()
percent.visualize_network()


# create mega network for topology version 1
df2 = pd.DataFrame(v1_mega_network)
v1_total_network = df2.sum()
v1_percentage_network = [float(i) for i in v1_total_network]

flow_in = v1_percentage_network[0]

for i in range(len(v1_percentage_network)):
    v1_percentage_network[i] = round(v1_percentage_network[i] / flow_in * 100, 2)

# build the network and visualize it
percent_v1 = v1.HCNetworkV1()
percent_v1.set_data(v1_percentage_network[0], v1_percentage_network[1], v1_percentage_network[2], v1_percentage_network[3], v1_percentage_network[4], v1_percentage_network[5], v1_percentage_network[6], v1_percentage_network[7], v1_percentage_network[8])
percent_v1.build_network()
percent_v1.visualize_network()
