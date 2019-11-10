import requests
import json

customerId = '5dc6e809322fa016762f363f'
apiKey = '32b4c33d3c73bb71a1116bba8c3df39e'

url = 'http://api.reimaginebanking.com/merchants?lat=40.8716978&lng=-74.0411163&rad=50&key={}'.format(apiKey)

json = requests.get(url).json()

mid = []
names = []
cat = []

mid_f = []
mid_h = []
mid_c = []
mid_e = []

food_words = ['restaurant', 'meal_takeaway', 'grocery_or_supermarket', 'meal_delivery', 'food', 'Groceries', 'bakery', 'cafe']
health_words = ['pharmacy', 'health', 'veterinary_care', 'pet_store']
clothing_words = ['department_store', 'shoe_store', 'clothing_store', 'shopping_mall', 'Department Store']
entertainment_word = ['bar', 'night_club', 'bowling_alley']

sum_words = food_words + health_words + clothing_words + entertainment_word

for i in json:
    if(i['name'] not in names and i['category'][0] in food_words):
        names.append(i['name'])
        mid_f.append(i["_id"])
        cat.append(i["category"])
    elif(i['name'] not in names and i['category'][0] in health_words):
        names.append(i['name'])
        mid_h.append(i["_id"])
        cat.append(i["category"])
    elif(i['name'] not in names and i['category'][0] in clothing_words):
        names.append(i['name'])
        mid_c.append(i["_id"])
        cat.append(i["category"])
    elif(i['name'] not in names and i['category'][0] in entertainment_word):
        names.append(i['name'])
        mid_e.append(i["_id"])
        cat.append(i["category"])

print(mid_f)
