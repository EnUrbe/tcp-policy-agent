from flask import Flask, request, jsonify
from services.openstates_api import search_state_bills
from services.congress_api import search_federal_bills

app = Flask(__name__)

@app.route('/api/state_bills', methods=['GET'])
def get_state_bills():
    state = request.args.get('state')
    keyword = request.args.get('keyword')
    results = search_state_bills(state, keyword)
    return jsonify(results)

@app.route('/api/federal_bills', methods=['GET'])
def get_federal_bills():
    keyword = request.args.get('keyword')
    results = search_federal_bills(keyword)
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)

