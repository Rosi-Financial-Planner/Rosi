# food, electricity, water, gas

import requests
import json
import random

customerId = '5dc715db322fa016762f3647'
apiKey = '226e5d0e1569a36825aafdd02fafb76e'

def create_merchants():

    url = 'http://api.reimaginebanking.com/merchants?key={}'.format(apiKey)
    payload = {
        "name": "New Jersey American Water",
        "category": "Water",
        "address": {
            "street_number": "104",
            "street_name": "Simon St",
            "city": "Hackensack",
            "state": "NJ",
            "zip": "07601"
        },
        "geocode": {
            "lat": 40.8716918,
            "lng": -74.0411123
        }
    }

    requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
    )

    payload = {
        "name": "PSE&G",
        "category": "Electric",
        "address": {
            "street_number": "214",
            "street_name": "Hudson St",
            "city": "Hackensack",
            "state": "NJ",
            "zip": "07601"
        },
        "geocode": {
            "lat": 40.8716978,
            "lng": -74.0411163
        }
    }

    requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
    )


def populate_purchases():
    elect_id = ["5dc72cc93c8c2216c9fcb896"]
    water_id = ["5dc72cc23c8c2216c9fcb895"]
    util_id = ["5dc72cc23c8c2216c9fcb895", "5dc72cc23c8c2216c9fcb896"]

    url = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}".format(customerId, apiKey)
    food_id = ["57cf75cea73e494d8675f5b4", "57cf75cea73e494d8675f5bb", "57cf75cea73e494d8675f5bd", "57cf75cea73e494d8675f5bf"]


    for i in range(10):
        mid = random.choice(food_id)
        price = random.randint(8,30)
        payload = {
            "merchant_id": mid,
            "medium": "balance",
            "purchase_date": "2019-11-09",
            "amount": price,
            "status": "completed",
            "description": "string"
        }

        requests.post( 
            url, 
            data=json.dumps(payload),
            headers={'content-type':'application/json'},
        )


    for i in range(4):
        mid = random.choice(util_id)
        price = random.randint(150,300)
        payload = {
            "merchant_id": mid,
            "medium": "balance",
            "purchase_date": "2019-11-09",
            "amount": price,
            "status": "completed",
            "description": "string"
        }

        requests.post( 
            url, 
            data=json.dumps(payload),
            headers={'content-type':'application/json'},
        )


populate_purchases()

