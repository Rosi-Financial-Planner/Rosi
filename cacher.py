import json
import apiScrape
import time
import os

custId = '5dc6e809322fa016762f363f'
key = '32b4c33d3c73bb71a1116bba8c3df39e'

os.mkdir['/tmp']
while 1:
    scraped = apiScrape.scrapeTheApi(custId, key)
    with open('cache.json', 'w') as fp:
        json.dump(scraped, fp)
    print("cached")
    time.sleep(60)
