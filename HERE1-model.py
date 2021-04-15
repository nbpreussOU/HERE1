import VAMCv0 as v0
import VAMCv1 as v1
import VAMCv3 as v3
import pandas as pd
import numpy as np
import random


def analyze_model(filename, name):
    # create a list to store all our values
    data = []
    mega_network = []
    x = name
    runs = 500

    # create n different networks and store the results
    for a in range(0, runs):
        # build network
        x.initialize()
        x.build_network()
        data.append(x.analyze_network())
        mega_network.append(x.get_data())

    # create a dataframe from the values we got and write it out to a csv
    df = pd.DataFrame(data, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
    df.to_csv("Data/" + filename + ".csv", index=False)

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
    percent.visualize_network(filename)

    # print out summary data for analysis
    analysis = [i/runs for i in df.sum()]

    # gather relevant data and store it in a csv
    j = list(df.max(axis=0))
    k = list(df.min(axis=0))
    j[3] = k[3]
    i = ["Flow In", "Flow Out", "Efficiency", "Longest Wait", "Total Wait"]
    out_data = pd.DataFrame(np.column_stack([i, analysis, j]), columns=['Metric', 'Mean', 'Extreme'])
    out_data.to_csv("Data/" + filename + "_metrics.csv", index=False)


def distribution():
    # super secret calculations looking at the effect of standard deviation on the metrics
    mean_data = []
    max_data = []
    runs = 500

    # do the runs over a range of standard deviations
    for i in range(0, 50):
        data = []
        # run the model a certain number of times
        for a in range(0, runs):
            x = v3.HCNetworkV3()
            x.initialize(i)
            x.build_network()
            data.append(x.analyze_network(i))

        # gather relevant data and store it in a csv
        df3 = pd.DataFrame(data)
        j = list(df3.max(axis=0))
        k = list(df3.min(axis=0))
        j[2] = k[2]
        mean_data.append(list(df3.mean(axis=0)))
        max_data.append(j)

    # create a dataframe from the values we got and write it out to a csv
    df_mean = pd.DataFrame(mean_data,
                           columns=['Standard Deviation', 'Flow In', 'Flow Out', 'Efficiency', 'Longest Wait',
                                    'Total Wait'])
    df_mean.to_csv("Data/v3_mean_data.csv", index=False)

    df_max = pd.DataFrame(max_data, columns=['Standard Deviation', 'Flow In', 'Flow Out', 'Efficiency', 'Longest Wait',
                                             'Total Wait'])
    df_max.to_csv("Data/v3_max_data.csv", index=False)


# setting seeds
random.seed(16)

# analyze the model and output it to a given csv file
analyze_model("Original Model", v0.HCNetworkV0())
analyze_model("Send Home", v1.HCNetworkV1())
distribution()
