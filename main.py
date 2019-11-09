# food, electricity, water, gas

import requests
import json

customerId = '5dc715db322fa016762f3647'
apiKey = '226e5d0e1569a36825aafdd02fafb76e'

url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)

json = requests.get(url).json()

account_id = json[0]['_id']
print(account_id)
purchases_url = 'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'.format(account_id, apiKey)
