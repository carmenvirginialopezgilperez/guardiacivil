from flask import Flask
import requests
from flask import Response, make_response
from flask import request, jsonify
import json
from flask_assistant import core
from flask_cors import cross_origin, CORS
import argparse


app = Flask(__name__)
cors = CORS(app)

if __name__ == "__main__":
	app.run()

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")
	

	
