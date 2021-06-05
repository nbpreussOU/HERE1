import VAMCv0 as v0
import VAMCv1 as v1
import VAMCv3 as v3
import pandas as pd
import numpy as np
from scipy import stats


def analyze_model(filename, name, runs):
    # create a list to store all our values
    metrics = []
    edges = []

    # create n different networks and store the results
    for a in range(runs):
        # build network
        name.initialize()
        name.build_network()
        metrics.append(name.analyze_network())
        edges.append(name.get_data())

    # create a dataframe from the values we got and write it out to a csv
    df = pd.DataFrame(metrics, columns=['Flow In', 'Flow Out', 'Efficiency', 'Longest Wait', 'Total Wait'])
    df2 = pd.DataFrame(edges)
    df3 = pd.DataFrame(pd.concat([df, df2], axis=1))

    # remove outliers
    df3 = df3[(np.abs(stats.zscore(df3["Flow In"])) < 3)]
    df3 = df3[(np.abs(stats.zscore(df3["Flow Out"])) < 3)]
    df3 = df3[(np.abs(stats.zscore(df3["Efficiency"])) < 3)]
    df3 = df3[(np.abs(stats.zscore(df3["Longest Wait"])) < 3)]
    df3 = df3[(np.abs(stats.zscore(df3["Total Wait"])) < 3)]

    # output data to csv
    df3.to_csv("Data/" + filename + ".csv", index=False)

    # create mega network for topology version
    total_network = df3.sum() / len(df3.index)
    percentage_network = [round(float(i), 3) for i in total_network]

    # build the network and visualize it
    name.set_data(percentage_network[5:])
    name.build_network()
    name.visualize_network(filename)

    # print out summary data for analysis
    analysis = [round(i/len(df3.index), 3) for i in df3.sum()]

    # gather relevant metrics and store it in a csv
    j = list(df3.max(axis=0))
    k = list(df3.min(axis=0))
    j[2] = k[2]
    i = ["Flow In", "Flow Out", "Efficiency", "Longest Wait", "Total Wait"]
    out_data = pd.DataFrame(np.column_stack([i, analysis[0:5], j[0:5]]), columns=['Metric', 'Mean', 'Extreme'])
    out_data.to_csv("Data/" + filename + "_metrics.csv", index=False)


def distribution(runs):
    # super secret calculations looking at the effect of standard deviation on the metrics
    mean_data = []
    max_data = []

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
        j[3] = k[3]
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


# analyze the model and output it to a given csv file
num_rums = 500
analyze_model("Original Model", v0.HCNetworkV0(), num_rums)
analyze_model("Send Home", v1.HCNetworkV1(), num_rums)
distribution(num_rums)
