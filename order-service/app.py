from flask import Flask, request
import psycopg
import os
import socket

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "microservices")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "admin123")


def get_db_connection():
    return psycopg.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


@app.route("/")
def home():
    return f"Order Service is running on container: {socket.gethostname()}"


@app.route("/orders", methods=["GET"])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, product, quantity FROM orders ORDER BY id")
    data = cur.fetchall()

    cur.close()
    conn.close()

    return f"Container: {socket.gethostname()} | Orders: {data}"


@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (product, quantity) VALUES (%s, %s) RETURNING id",
        (data["product"], data["quantity"])
    )

    order_id = cur.fetchone()[0]
    conn.commit()

    cur.close()
    conn.close()

    return f"Order created with ID: {order_id}", 201


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE orders SET product = %s, quantity = %s WHERE id = %s RETURNING id",
        (data["product"], data["quantity"], order_id)
    )

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return "Order not found", 404

    conn.commit()

    cur.close()
    conn.close()

    return f"Order {order_id} updated successfully", 200


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM orders WHERE id = %s RETURNING id",
        (order_id,)
    )

    result = cur.fetchone()

    if result is None:
        cur.close()
        conn.close()
        return "Order not found", 404

    conn.commit()

    cur.close()
    conn.close()

    return f"Order {order_id} deleted successfully", 200


app.run(host="0.0.0.0", port=8002)
