from flask import Flask, render_template, jsonify
import json
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/spots")
def get_spots():
    with open("status.json") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)