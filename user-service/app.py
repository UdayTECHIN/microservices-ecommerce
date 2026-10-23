from flask import Flask
import socket

app = Flask(__name__)

@app.route("/")
def home():
    return f"User Service v3 is running | Container: {socket.gethostname()}"

@app.route("/users")
def users():
    return f"Users: Uday, Rahul, Amit | Version: v3 | Container: {socket.gethostname()}"

app.run(host="0.0.0.0", port=8001)
