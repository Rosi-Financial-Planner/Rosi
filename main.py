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
                        datetime.date.fromisoformat(
                            deposit["transaction_date"]),
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
                        datetime.date.fromisoformat(
                            withdrawal["transaction_date"]),
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
                        datetime.date.fromisoformat(
                            transfer["transaction_date"]),
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
                        datetime.date.fromisoformat(bill["payment_date"]),
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
                        datetime.date.fromisoformat(purchase["purchase_date"]),
                        payee,
                        merchantCategory,
                        -purchase["amount"]
                    ]
                    )

print(events)
