<<<<<<< HEAD
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
=======
import requests
import datetime

customerId = '5dc6e809322fa016762f363f'
apiKey = '32b4c33d3c73bb71a1116bba8c3df39e'

accountsUrl = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'\
        .format(customerId, apiKey)
accountsRequest = requests.get(accountsUrl)
accountsJson = accountsRequest.json()

numAccounts = len(accountsJson)
accounts = {}
for account in accountsJson:
    accounts[account['_id']] = account['balance']
print(accounts)

# Make a set of ordered triples for each account in the form
# [date, payee, amount]

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
        if deposit["status"] == "executed":
            events[account].append(
                    [
                        datetime.date.fromisoformat(
                            deposit["transaction_date"]),
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
        if withdrawal["status"] == "executed":
            events[account].append(
                    [
                        datetime.date.fromisoformat(
                            withdrawal["transaction_date"]),
                        None,
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
        if transfer["status"] == "executed":
            transferAmount = transfer["amount"]
            if transfer["payer_id"] == account:
                transferAmount = -transferAmount
            events[account].append(
                    [
                        datetime.date.fromisoformat(
                            transfer["transaction_date"]),
                        None,
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
        if bill["status"] == "executed" or bill["status"] == "recurring":
            payee = bill["payee"]
            events[account].append(
                    [
                        datetime.date.fromisoformat(bill["transaction_date"]),
                        payee,
                        -bill["amount"]
                    ]
                    )
    # Purchases
    purchasesUrl = \
        'http://api.reimaginebanking.com/accounts/{}/purchases?key={}'\
        .format(account, apiKey)
    purchasesRequest = requests.get(purchasesUrl)
    purchasesJson = purchasesRequest.json()
    for purchase in purchasesJson:
        if purchase["status"] == "executed":
            merchantID = purchase["merchant_id"]

            merchantUrl = \
                'http://api.reimaginebanking.com/merchants/{}?key={'\
                .format(merchantID, apiKey)
            merchantRequest = requests.get(merchantUrl)
            merchantJson = merchantRequest.json()
            payee = merchantJson["name"]

            events[account].append(
                    [
                        datetime.date.fromisoformat(purchase["purchase_date"]),
                        payee,
                        -purchase["amount"]
                    ]
                    )

print(events)
>>>>>>> ec7093990f5f36e8e0315bc453056d2851f5cb55
