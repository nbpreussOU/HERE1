import hcnetwork
import pandas as pd

# create a list to store all our values
data = []
mega_network = []

# create 30 different networks and store the results
for a in range(0, 100):
    x = hcnetwork.HCNetwork()
    x.build_network()
    data.append(x.analyze_network())
    # x.visualize_network()
    mega_network.append(x.get_data())

# create a dataframe from the values we got and write it out to a csv
df = pd.DataFrame(data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
df.to_csv(r'temp.csv', index=False)

# create mega network
df2 = pd.DataFrame(mega_network)
total_network = df2.sum()
percentage_network = [float(i) for i in total_network]

flow_in = percentage_network[0]

for i in range(len(percentage_network)):
    percentage_network[i] = round(percentage_network[i] / flow_in * 100, 2)

# build the network and visualize it
percent = hcnetwork.HCNetwork()
percent.set_data(percentage_network[0], percentage_network[1], percentage_network[2], percentage_network[3], percentage_network[4], percentage_network[5], percentage_network[6], percentage_network[7])
percent.build_network()
print(percent.analyze_network())
percent.visualize_network()
