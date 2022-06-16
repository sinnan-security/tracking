from flask import Flask,jsonify,request,make_response
from urllib.parse import urlparse
import dotenv
import psutil
import requests
import random
import string
import datetime
app = Flask(__name__)
config=dotenv.dotenv_values("/etc/#name.conf")
rand="".join(random.choices(string.ascii_uppercase + string.digits, k=5))

@app.route('/api/tracking/SomeRoute', methods=['GET'])
@app.route('/api/tracking/SomeRoute', methods=['POST'])
@app.route('/api/tracking/SomeRoute', methods=['PUT'])
@app.route('/api/tracking/SomeRoute', methods=['DELETE'])
def SomeFunctionality():
	response={}
	return "<h1>tracking service %%s</H1>"%%(rand)

if __name__ == "__main__":
	app.run(host=config["host"],port=config["port"])

