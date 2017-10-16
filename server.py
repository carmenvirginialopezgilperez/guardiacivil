from flask import Flask
import requests
from flask import Response
from flask import request, jsonify
import json
from flask_cors import cross_origin, CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/')
def index():
	return 'Yo, its working!'

#http://127.0.0.1:5000/vehiculo/?matricula=12
@app.route('/vehiculo', methods=["POST"])
def vehiculo_preguntar():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["matricula"]
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/vehiculo/?matricula='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["properties"]
	respuesta_modelo = respuesta_pro["modelo"]
	respuesta_marca1 = respuesta_pro["marca"]
	respuesta_marca = respuesta_marca1["descripcionLarga"]
	respuesta_bastidor = respuesta_pro["numeroBastidor"]
	respuesta_color1 = respuesta_pro["colorPrimario"]
	respuesta_color = respuesta_color1["descripcionLarga"]
	respuesta_matricula = respuesta_pro["matricula"]
	final = "El vehículo con matricula "+respuesta_matricula+"es de la marca"+respuesta_marca+" su modelo es "+respuesta_modelo+" de color "+respuesta_color+" y con número de bastidor "+respuesta_bastidor+"."
	final_texto = { "speech": final, "displayText": final, "data": {},"contextOut": [],"source": "" }
	#final_texto['Body'] = final_texto
	json_data_final = json.dumps(final_texto)
	#return Response(headers={'Content-type': 'application/json'}, body=final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")


@app.route('/alias', methods=["POST"])
def persona_preguntar():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["dni"]
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

	
