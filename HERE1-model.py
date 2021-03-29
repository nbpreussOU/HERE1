import VAMCv0 as v0
import VAMCv1 as v1
import pandas as pd


def analyze_model(filename, name):
    # create a list to store all our values
    data = []
    mega_network = []
    x = name

    # create 100 different networks and store the results
    for a in range(0, 100):
        # build network
        x.initialize()
        x.build_network()
        data.append(x.analyze_network())
        mega_network.append(x.get_data())

    # create a dataframe from the values we got and write it out to a csv
    df = pd.DataFrame(data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
    df.to_csv(filename, index=False)

    # create mega network for topology version
    df2 = pd.DataFrame(mega_network)
    total_network = df2.sum()
    percentage_network = [float(i) for i in total_network]

    # round data
    flow_in = percentage_network[0]
    for i in range(len(percentage_network)):
        percentage_network[i] = round(percentage_network[i] / flow_in * 100, 2)

    # build the network and visualize it
    percent = name
    percent.set_data(percentage_network)
    percent.build_network()
    percent.visualize_network()


# analyze the model and output it to a given csv file
analyze_model("v0_data.csv", v0.HCNetworkV0())
analyze_model("v1_data.csv", v1.HCNetworkV1())
