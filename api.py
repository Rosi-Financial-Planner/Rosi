import flask
import apiScrape
import os
import tips

customerId = '5dc6e809322fa016762f363f'
apiKey = '32b4c33d3c73bb71a1116bba8c3df39e'
accountId = '5dc6e80d322fa016762f3644'

app = flask.Flask(__name__)
app.config["DEBUG"] = False

cache = {}
knownTransactions = []


@app.route('/', methods=['GET'])
def home():
    return "An API for getting data about your transactions with Capital One"


@app.route('/entries/all', methods=['GET'])
def api_all():
    return cache


@app.route('/entries', methods=['GET'])
def api_recent():
    if 'months' in flask.request.args:
        months = int(flask.request.args['months'])
    else:
        return """Error: Give a number of
                  months in the past from which to draw data"""

    return apiScrape.monthFilter(cache, months)


@app.route('/entries/simple', methods=['GET'])
def api_simple():
    return apiScrape.simplifyToCharges(cache)


@app.route('/entries/update', methods=['GET'])
def update():
    global cache
    global knownTransactions
    cache = apiScrape.scrapeTheApi(customerId, apiKey)
    for i in knownTransactions:
        cache[accountId][knownTransactions["index"]][2]\
                = knownTransactions["type"]

    apiScrape.findUnknowns(cache)
    return cache


@app.route('/tips', methods=['GET'])
def get_tips():
    return tips.get_tips(cache)


@app.route('/twilio', methods=['POST'])
def get_type():
    global knownTransactions
    # dictionary with entries index and type
    index = flask.request.form['index']
    transactionType = flask.request.form['type']
    cache[accountId][index][2] = transactionType
    knownTransactions.append({"index": index, "type": transactionType})


port = int(os.environ.get('PORT'))
app.run(host='0.0.0.0', port=port)
