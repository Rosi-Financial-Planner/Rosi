import pandas as pd
from datetime import date

food_words = ['restaurant', 'meal_takeaway', 'grocery_or_supermarket', 'meal_delivery', 'food', 'Groceries', 'bakery', 'cafe']
clothing_words = ['department_store', 'shoe_store', 'clothing_store', 'shopping_mall', 'Department Store']
entertainment_word = ['bar', 'night_club', 'bowling_alley']

dataPath = "datasets/"

def sum_cost(events):
    sum_el = sum_water = sum_food = sum_clo = sum_ent = 0

    sums = {
        "1": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "2": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "3": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "4": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "5": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "6": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "7": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "8": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "9": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "10": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "11": [sum_el, sum_water, sum_food, sum_clo, sum_ent],
        "12": [sum_el, sum_water, sum_food, sum_clo, sum_ent]
    }

    for i in events:
        for j in events[i]:
            print(j)
            for month in range(1, 13):
                if(j[0][5:7] == str(month) and j[1] == "Electricity bill"):
                    sums[str(month)][0] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[1] == "Water bill"):
                    sums[str(month)][1] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2] in food_words):
                    sums[str(month)][2] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2] in clothing_words):
                    sums[str(month)][3] += abs(j[3])
                elif(j[0][5:7] == str(month) and j[2] in entertainment_word):
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
        return "Last month, you spent: $" + str(month_sum) + " on your electric bill. \nYour electricity bill is " \
             + str(round(percent_dif, 1)) + "% higher than your local average. \nYou can find out more information on how to reduce your electric bill here: https://paylesspower.com/blog/how-to-lower-your-electric-bill/"
    else:
        return None
    

def water_tip(month_sum, avg = 53.41):
    percent_dif = (month_sum - avg) / avg * 100
    if(percent_dif > 20):
        return "Last month, you spent: $" + str(month_sum) + " on your water bill. \nYour water bill is " \
             + str(round(percent_dif, 1)) + "% higher than your local average. \nYou can find out more information on how to reduce your water bill here: https://money.usnews.com/money/blogs/my-money/2012/10/16/6-simple-ways-to-save-money-on-your-water-bill"
    else:
        return None

def food_tip(month_sum, avg = 425):
    percent_dif = (month_sum - avg) / avg * 100
    if(percent_dif > 20):
        return "Last month, you spent: $" + str(month_sum) + " on food expenses. \nTo save money, we recommend spending no more than " \
             + avg + "per month. \nSave money by spending less money on restaurants and instead buying groceries more often."
    else:
        return None

def execute(events):
    state = "NJ"
    path = dataPath
    state_avg = electricity_cost(path, state)
    sums = sum_cost(events)
    last_month = str(int(str(date.today())[5:7]) - 1)
    print(elec_tip(state_avg, sums[last_month][0]))
    print(water_tip(sums[last_month][1]))
    print(food_tip(sums[last_month][2]))

def get_tips(events):
    state = "NJ"
    path = dataPath
    state_avg = electricity_cost(path, state)
    sums = sum_cost(events)
    last_month = str(int(str(date.today())[5:7]) - 1)
    tips = {}
    tips["elec"] = elec_tip(state_avg, sums[last_month][0])
    tips["water"] = water_tip(sums[last_month][1])
    tips["food"] = food_tip(sums[last_month][2])
    return tips

if(__name__ == "__main__"):
    pass
    
