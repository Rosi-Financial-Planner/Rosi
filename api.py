import flask
import apiScrape
import json
import os

customerId = '5dc6e809322fa016762f363f'
apiKey = '32b4c33d3c73bb71a1116bba8c3df39e'

app = flask.Flask(__name__)
app.config["DEBUG"] = False


@app.route('/', methods=['GET'])
def home():
    return "An API for getting data about your transactions with Capital One"


@app.route('/entries/all', methods=['GET'])
def api_all():
    return json.dumps(apiScrape.cacheLoad())


@app.route('/entries', methods=['GET'])
def api_recent():
    if 'months' in flask.request.args:
        months = int(flask.request.args['months'])
    else:
        return """Error: Give a number of
                  months in the past from which to draw data"""

    return apiScrape.cacheMonthScrape(months)


@app.route('/entries/simple', methods=['GET'])
def api_simple():
    return json.dumps(apiScrape.simplifyToCharges(apiScrape.cacheLoad()))


port = int(os.environ.get('PORT'))
app.run(host='0.0.0.0', port=port)
