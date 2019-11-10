import requests
import json
import datetime

cache = "cache.json"


def scrapeTheApi(customerId, apiKey):
    accountsUrl = \
        'http://api.reimaginebanking.com/customers/{}/accounts?key={}'\
        .format(customerId, apiKey)
    accountsRequest = requests.get(accountsUrl)
    accountsJson = accountsRequest.json()

    accounts = {}
    for account in accountsJson:
        accounts[account['_id']] = account['balance']

    # Make a set of ordered quadruples for each account in the form
    # [date, payee, category, amount]

    events = {}
    for account in accounts.keys():
        events[account] = []
        # Deposits
        depositsUrl = \
            'http://api.reimaginebanking.com/accounts/{}/deposits?key={}'\
            .format(account, apiKey)
        depositsRequest = requests.get(depositsUrl)
        depositsJson = depositsRequest.json()
        for deposit in depositsJson:
            if deposit["status"] != "cancelled":
                events[account].append(
                        [
                            deposit["transaction_date"],
                            "Deposit",
                            "Deposit",
                            deposit["amount"]
                        ]
                        )
        # Withdrawals
        withdrawalsUrl = \
            'http://api.reimaginebanking.com/accounts/{}/withdrawals?key={}'\
            .format(account, apiKey)
        withdrawalsRequest = requests.get(withdrawalsUrl)
        withdrawalsJson = withdrawalsRequest.json()
        for withdrawal in withdrawalsJson:
            if withdrawal["status"] != "cancelled":
                events[account].append(
                        [
                            withdrawal["transaction_date"],
                            None,
                            "Withdrawal",
                            -withdrawal["amount"]
                        ]
                        )
        # Transfers
        transferUrl = \
            'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'\
            .format(account, apiKey)
        transfersRequest = requests.get(transferUrl)
        transfersJson = transfersRequest.json()
        for transfer in transfersJson:
            if transfer["status"] != "cancelled":
                transferAmount = transfer["amount"]
                if transfer["payer_id"] == account:
                    transferAmount = -transferAmount
                events[account].append(
                        [
                            transfer["transaction_date"],
                            None,
                            "Transfer",
                            transferAmount
                        ]
                        )
        # Bills
        billsUrl = \
            'http://api.reimaginebanking.com/accounts/{}/bills?key={}'\
            .format(account, apiKey)
        billsRequest = requests.get(billsUrl)
        billsJson = billsRequest.json()
        for bill in billsJson:
            if bill["status"] != "cancelled":
                payee = bill["payee"]
                events[account].append(
                        [
                            bill["payment_date"],
                            payee,
                            "Bill",
                            -bill["payment_amount"]
                        ]
                        )
        # Purchases
        purchasesUrl = \
            'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'\
            .format(account, apiKey)
        purchasesRequest = requests.get(purchasesUrl)
        purchasesJson = purchasesRequest.json()
        for purchase in purchasesJson:
            if purchase["status"] != "cancelled":
                merchantID = purchase["merchant_id"]

                merchantUrl = \
                    'http://api.reimaginebanking.com/merchants/{}?key={}'\
                    .format(merchantID, apiKey)
                merchantRequest = requests.get(merchantUrl)
                merchantJson = merchantRequest.json()
                payee = merchantJson["name"]
                merchantCategory = merchantJson["category"]

                events[account].append(
                        [
                            purchase["purchase_date"],
                            payee,
                            merchantCategory,
                            -purchase["amount"]
                        ]
                        )
    return events


def simplifyToCharges(events):
    output = {}
    for key in events.keys():
        output[key] = []
        for event in events[key]:
            output[key].append([event[0], event[3]])
    return output


def jsonSimple(customerId, apiKey):
    return json.dumps(simplifyToCharges(scrapeTheApi(customerId, apiKey)))


def jsonScrape(customerId, apiKey):
    return json.dumps(scrapeTheApi(customerId, apiKey))


def jsonMonthScrape(customerId, apiKey, months):
    output = {}
    currentDate = datetime.date.today()
    currentMonth = currentDate.month
    currentYear = currentDate.year
    targetMonth = currentMonth - months % 12
    if currentMonth < months:
        targetYear = currentYear - 1
    else:
        targetYear = currentYear

    scraped = scrapeTheApi(customerId, apiKey)
    for key in scraped.keys():
        output[key] = []
        for event in scraped[key]:
            eventYear = int(event[0][0:4])
            eventMonth = int(event[0][5:7])
            if eventYear >= targetYear:
                if eventMonth >= targetMonth:
                    output[key].append(event)
    return json.dumps(output)


def cacheLoad():
    with open('cache.json', 'r') as fp:
        return json.load(fp)


def cacheMonthScrape(months):
    output = {}
    currentDate = datetime.date.today()
    currentMonth = currentDate.month
    currentYear = currentDate.year
    targetMonth = currentMonth - months % 12
    if currentMonth < months:
        targetYear = currentYear - 1
    else:
        targetYear = currentYear

    scraped = cacheLoad()
    for key in scraped.keys():
        output[key] = []
        for event in scraped[key]:
            eventYear = int(event[0][0:4])
            eventMonth = int(event[0][5:7])
            if eventYear >= targetYear:
                if eventMonth >= targetMonth:
                    output[key].append(event)
    return json.dumps(output)


if __name__ == "__main__":
    custId = '5dc6e809322fa016762f363f'
    key = '32b4c33d3c73bb71a1116bba8c3df39e'

    scraped = scrapeTheApi(custId, key)
    simplified = simplifyToCharges(scraped)

    with open('result.json', 'w') as fp:
        json.dump(simplified, fp)
