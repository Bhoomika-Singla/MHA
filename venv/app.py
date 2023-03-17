from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "Hello World"

@app.route("/query", methods=['GET'])
def query():
    if request.method == 'GET':
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        attributes = request.args.getlist('attr')

        to_return = jsonify(start_date=start_date, end_date=end_date, attributes=attributes)
        return to_return