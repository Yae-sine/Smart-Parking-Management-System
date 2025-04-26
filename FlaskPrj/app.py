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
    try:
        with open("../AI/status.json") as f:
            data = json.load(f)
        return jsonify(data)
    except:
        return jsonify({})

if __name__ == "_main_":
    app.run(debug=True, host='0.0.0.0',port=5000)