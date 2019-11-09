import pandas as pd

def electricity_cost(path, state, base = 915):
    df = pd.read_csv(path + "electricity.csv", header=None)
    state_row = df.loc[df[0] == state]
    price_kwh = state_row[1].values[0]
    price = round(price_kwh * base / 100, 2)
    return price




if(__name__ == "__main__"):
    path = "C://Users//Rahul//Desktop//Rosi//datasets//"
    print(electricity_cost(path, "NJ"))