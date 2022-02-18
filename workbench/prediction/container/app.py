from flask import Flask, request, jsonify
from prediction import predict

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def index():
    json_data = request.json
    kwarg = json_data["parameters"]
    instances = json_data["instances"]
    results = []
    for instance in instances:
        results.append(predict(instance, **kwarg))
    response = {
        "predictions": results
    }
    return jsonify(response)


@app.route("/ping")
def ping():
    return "pong"