import numpy as np


def preprocess(data):
    data = data.replace(np.nan, 0)
    # Value, Wage, Release Clause(Million)
    data["Value"] = data["Value"].str.replace("€", "").astype(str)
    data["Release Clause"] = data["Release Clause"].str.replace("€", "").astype(str)
    for i, row in data.iterrows():
        if row["Value"][-1] == 'K':
            row["Value"] = row["Value"].replace('K', '')
            t = float(row["Value"])
            row["Value"] = str(t / 1000)
            data.at[i, "Value"] = str(t / 1000)

        if row["Release Clause"][-1] == 'K':
            row["Release Clause"] = row["Release Clause"].replace('K', '')
            t = float(row["Release Clause"])
            row["Release Clause"] = str(t / 1000)
            data.at[i, "Release Clause"] = str(t / 1000)

    data["Value(€ Million)"] = data["Value"].str.replace("M", "").astype(float)
    data["Value"] = data["Value"].str.replace("M", "").astype(float)
    data["Release Clause(€ Million)"] = data["Release Clause"].str.replace("M", "").astype(float)
    data["Release Clause"] = data["Release Clause"].str.replace("M", "").astype(float)

    data["Wage"] = data["Wage"].str.replace("€", "")
    data["Wage"] = data["Wage"].str.replace("K", "").astype(float)
    data["Wage"] = data["Wage"] / 1000
    data["Wage(€ Million)"] = data["Wage"]

    # Weight(lbs)
    data["Weight"] = data["Weight"].str.replace("lbs", "")
    data["Weight(lbs)"] = data["Weight"].str.replace("lbs", "")
    # Height(cm)
    for i, row in data.iterrows():
        height_list = row.Height.split("'")
        cm = (float(height_list[0]) * 12 + float(height_list[1])) * 2.54
        data.at[i, "Height(cm)"] = cm
        data.at[i, "Height"] = cm

    # get skill's number
    cols = ['LS', 'ST', 'RS', 'LW', 'LF', 'CF', 'RF', 'RW',
            'LAM', 'CAM', 'RAM', 'LM', 'LCM', 'CM', 'RCM', 'RM', 'LWB', 'LDM',
            'CDM', 'RDM', 'RWB', 'LB', 'LCB', 'CB', 'RCB', 'RB']
    for i, row in data.iterrows():
        for column in cols:
            data.at[i, column] = eval(str(row[column]))
    for column in cols:
        data[column] = data[column].astype(float)

    return data
