import hcnetwork
import pandas as pd

# create a list to store all our values
data = []

# create 30 different networks and store the results
for a in range(0, 100):
    x = hcnetwork.HCNetwork()
    x.build_network()
    data.append(x.analyze_network())
    # x.visualize_network()

# create a dataframe from the values we got and write it out to a csv
df = pd.DataFrame(data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
df.to_csv(r'temp.csv', index=False)
