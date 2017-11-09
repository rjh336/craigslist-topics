import pandas as pd
from flask import Flask
from flask import render_template
import json
import numpy as np

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/data")
def get_data():
	df = pd.read_json('./data/app_data.json')
	return df.to_json(orient='records')

if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5000, debug=True)