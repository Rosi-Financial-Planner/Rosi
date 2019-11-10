import pandas as pd
from datetime import date

# events = {"abcd":
#     [
#         ["2019-11-09", "PSE&G", "Bill", 300], 
#         ["2019-11-10", "American Water", "Bill", 250],
#         ["2019-10-06", "Moe's", "Food", 10],
#         ["2019-11-09", "Chipotle", "Food", 30],
#         ["2019-11-09", "PSE&G", "Bill", 100],
#         ["2019-10-09", "PSE&G", "Bill", 200],
#         ["2019-10-09", "AMC Theatre", "Entertainment", 40],

#     ]
# }

def sum_cost(events):
    sum_el = sum_water = sum_grocery = sum_dept = sum_restaurant = 0

    sums = {
        "1": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "2": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "3": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "4": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "5": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "6": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "7": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "8": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "9": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "10": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "11": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant],
        "12": [sum_el, sum_water, sum_grocery, sum_dept, sum_restaurant]
    }

    for i in events:
        for j in events[i]:
            print(j)
            for month in range(1, 13):
                if(j[0][5:7] == str(month) and j[1] == "Electricity bill"):
                    sums[str(month)][0] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[1] == "Water bill"):
                    sums[str(month)][1] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2][0] == "grocery_or_supermarket"):
                    sums[str(month)][2] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2] == "department_store"):
                    sums[str(month)][3] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2] == "restaurant"):
                    sums[str(month)][4] += abs(j[3])
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
        print("Last month, you spent: $" + str(month_sum) + " on your electric bill. \nYour electricity bill is " \
             + str(round(percent_dif, 1)) + "% higher than your local average. \nYou can find out more information on how to reduce your electric bill here: https://paylesspower.com/blog/how-to-lower-your-electric-bill/")
    

def water_tip(month_sum, avg = 53.41):
    percent_dif = (month_sum - avg) / avg * 100
    if(percent_dif > 20):
        print("Last month, you spent: $" + str(month_sum) + " on your water bill. \nYour water bill is " \
             + str(round(percent_dif, 1)) + "% higher than your local average. \nYou can find out more information on how to reduce your water bill here: https://money.usnews.com/money/blogs/my-money/2012/10/16/6-simple-ways-to-save-money-on-your-water-bill")
        

def execute(events):
    state = "NJ"
    path = "C://Users//Rahul//Desktop//Rosi//datasets//"
    state_avg = electricity_cost(path, state)
    sums = sum_cost(events)
    last_month = str(int(str(date.today())[5:7]) - 1)
    elec_tip(state_avg, sums[last_month][0])
    water_tip(sums[last_month][1])


if(__name__ == "__main__"):
    pass
    
