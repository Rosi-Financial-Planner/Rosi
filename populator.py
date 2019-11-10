# food, electricity, water, gas

import requests
import json
import random
import datetime
import mid_repo

customerId = '5dc6e809322fa016762f363f'
accountId = '5dc6e80d322fa016762f3644'
apiKey = '32b4c33d3c73bb71a1116bba8c3df39e'


def randomDate(daysInThePast):
    d = datetime.timedelta(days=random.randrange(0, daysInThePast, 1))
    return datetime.date.today() - d


def deposit(amount):
    url = "http://api.reimaginebanking.com/accounts/{}/deposits?key={}"\
        .format(accountId, apiKey)

    payload = {
            "medium": "balance",
            "transaction_date": randomDate(1000).isoformat(),
            "status": "completed",
            "amount": amount
            }
    requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
            )


def populate_purchases(n):

    url = "http://api.reimaginebanking.com/accounts/{}/purchases?key={}"\
        .format(accountId, apiKey)
    # food_id = ["57cf75cea73e494d8675f5ab", "57cf75cea73e494d8675f5b2",
    #            "57cf75cea73e494d8675f5b5", "57cf75cea73e494d8675f5cd",
    #            "57cf75cea73e494d8675f5ca", "57cf75cea73e494d8675f5cc"]

    for i in range(n):
        # mid = random.choice(food_id)
        # price = random.randint(8, 30)
        price, mid = mid_repo.select_random()
        payload = {
            "merchant_id": mid,
            "medium": "balance",
            "purchase_date": randomDate(100).isoformat(),
            "amount": price,
            "status": "completed",
            "description": "string"
        }

        requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
        )


def populate_bills(n):
    billUrl = "http://api.reimaginebanking.com/accounts/{}/bills?key={}"\
        .format(accountId, apiKey)

    for i in range(n):
        payload = {
            "payment_date": (datetime.date.today() -
                             datetime.timedelta(days=30*i)).isoformat(),
            "payment_amount": random.randint(75, 100),
            "status": "pending",
            "payee": "Water bill"
        }

        requests.post(
            billUrl,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
        )

        payload = {
            "payment_date": (datetime.date.today() -
                             datetime.timedelta(days=30*i)).isoformat(),
            "payment_amount": random.randint(160, 300),
            "status": "pending",
            "payee": "Electricity bill"
        }

        requests.post(
            billUrl,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
        )


deposit(100000)
populate_purchases(150)
populate_bills(10)
