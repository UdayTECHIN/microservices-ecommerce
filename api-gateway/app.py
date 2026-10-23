from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/")
def home():
    return "API Gateway is running"


@app.route("/users")
def users():
    response = requests.get("http://user-service:8001/users")
    return response.text, response.status_code


@app.route("/orders", methods=["GET"])
def get_orders():
    response = requests.get("http://order-service:8002/orders")
    return response.text, response.status_code


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    response = requests.post(
        "http://order-service:8002/orders",
        json=data
    )

    return response.text, response.status_code


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()

    response = requests.put(
        f"http://order-service:8002/orders/{order_id}",
        json=data
    )

    return response.text, response.status_code


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    response = requests.delete(
        f"http://order-service:8002/orders/{order_id}"
    )

    return response.text, response.status_code


app.run(host="0.0.0.0", port=3000)
