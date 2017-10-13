from flask import Flask
import requests
from flask import Response
from flask import request
import json
app = Flask(__name__)
@app.route('/')
def index():
	return 'Yo, its working!'

#http://127.0.0.1:5000/vehiculo/?matricula=12
@app.route('/vehiculo', methods=["POST"])
def vehiculo_preguntar():
	text_un = request.json["matricula"]
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/vehiculo/?matricula='
	url_final = url + text_un
	return requests.get(url_final).content
	# Response(json_data, status=200, mimetype="application/json")


@app.route('/alias', methods=["POST"])
def persona_preguntar():
	text_un = request.json["dni"]
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/alias/?dni='
	url_final = url + text_un
	return requests.get(url_final).content

@app.route('/auxilio/', methods=["GET"])
def crear_auxilio():
	args = request.args
	text_gps = args.get("lugares", None)
	text_fecha = args.get("fechaConocimiento", None)
	text_persona = args.get("nombre", None)
	text_un = {"properties": { "lugares": {text_gps}, "fechaConocimiento": text_fecha, "nombre": text_persona}}
	json_data = json.dumps(text_un)
	url = 'http://104.154.101.83/alias/?dni='
	url_final = url + text_un
	return requests.get(url_final).content

@app.route('/avistamiento/', methods=["GET"])
def crear_avistamiento():
	args = request.args
	text_gps = args.get("lugares", None)
	text_fecha = args.get("fechaConocimiento", None)
	text_persona = args.get("nombre", None)
	text_un = {"properties": { "lugares": {text_gps}, "fechaConocimiento": text_fecha, "nombre": text_persona}}
	json_data = json.dumps(text_un)
	url = 'http://104.154.101.83/alias/?dni='
	url_final = url + text_un
	return requests.get(url_final).content


if __name__ == "__main__":
	app.run()
