from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)


@app.route("/hello")
def hello():
    print(request.headers)
    return jsonify({"success": True, "message": "hello, world!"})

