import pandas as pd
from datetime import date


# get customer state
state = "NJ"


events = {"abcd":
    [
        ["2019-11-09", "PSE&G", "Bill", 300], 
        ["2019-11-10", "American Water", "Bill", 250],
        ["2019-10-06", "Moe's", "Food", 10],
        ["2019-11-09", "Chipotle", "Food", 30],
        ["2019-11-09", "PSE&G", "Bill", 100],
        ["2019-10-09", "PSE&G", "Bill", 200],
        ["2019-10-09", "AMC Theatre", "Entertainment", 40],

    ]
}

def sum_cost(events):
    sum_el = sum_water = sum_food = sum_entertainment = 0

    sums = {
        "1": [sum_el, sum_water, sum_food, sum_entertainment],
        "2": [sum_el, sum_water, sum_food, sum_entertainment],
        "3": [sum_el, sum_water, sum_food, sum_entertainment],
        "4": [sum_el, sum_water, sum_food, sum_entertainment],
        "5": [sum_el, sum_water, sum_food, sum_entertainment],
        "6": [sum_el, sum_water, sum_food, sum_entertainment],
        "7": [sum_el, sum_water, sum_food, sum_entertainment],
        "8": [sum_el, sum_water, sum_food, sum_entertainment],
        "9": [sum_el, sum_water, sum_food, sum_entertainment],
        "10": [sum_el, sum_water, sum_food, sum_entertainment],
        "11": [sum_el, sum_water, sum_food, sum_entertainment],
        "12": [sum_el, sum_water, sum_food, sum_entertainment],
    }

    for i in events:
        for j in events[i]:
            for month in range(1, 13):
                if(j[0][5:7] == str(month) and j[1] == "PSE&G"):
                    sums[str(month)][0] += j[3]
                elif(j[0][5:7] == str(month) and j[1] == "American Water"):
                    sums[str(month)][1] += j[3]
                elif(j[0][5:7] == str(month) and j[2] == "Food"):
                    sums[str(month)][2] += j[3]
                elif(j[0][5:7] == str(month) and j[2] == "Entertainment"):
                    sums[str(month)][3] += j[3]

    return sums
    # print(sums["10"][2])

def electricity_cost(path, state, base = 915):
    df = pd.read_csv(path + "electricity.csv", header=None)
    state_row = df.loc[df[0] == state]
    price_kwh = state_row[1].values[0]
    price = round(price_kwh * base / 100, 2)
    return price

def elec_tip(avg, month_sum):
    percent_dif = (month_sum - avg) / avg * 100
    if(percent_dif > 20):
        print("Your electricity bill is much higher than the average compared to individuals in your area. Last month, you spent: " + str(month_sum) + " on your month bill. This is " + str(round(percent_dif, 1)) + "% more than the average. You can reduce costs by turning off lights in unused rooms.")
    





if(__name__ == "__main__"):
    path = "C://Users//Rahul//Desktop//Rosi//datasets//"
    state_avg = electricity_cost(path, state)
    sums = sum_cost(events)
    last_month = str(int(str(date.today())[5:7]) - 1)
    elec_tip(state_avg, sums[last_month][0])
    
