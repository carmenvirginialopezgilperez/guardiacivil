from flask import Flask
import requests
from flask import Response, make_response
from flask import request, jsonify
import json
from flask_assistant import core
from flask_cors import cross_origin, CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=["POST"])
def index():
	response_index = ""
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_consulta = text_pa["consulta"]
	print(text_consulta)
	if text_consulta == "1":
		response_index = persona_preguntar()
	if text_consulta == "2":
		print("consulta vehiculo")
		response_index = vehiculo_preguntar()
		
	print(response_index)	
	return response_index

@app.route('/vehiculos', methods=["POST"])
def vehiculo_preguntar():
	#text_total1 = request.json
	#text_result1 = text_total1["result"]
	#text_pa1 = text_result1["parameters"]
	text_un = text_pa["matricula"]
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/vehiculos/?matricula='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
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
	final = "El vehículo con matricula "+respuesta_matricula+"es de la marca "+respuesta_marca+" su modelo es "+respuesta_modelo+" de color "+respuesta_color+" y con número de bastidor "+respuesta_bastidor+"."
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	print(json_data_final)
	return Response(json_data_final, status=200, mimetype="application/json")


@app.route('/alias', methods=["POST"])
def persona_preguntar():
	#text_total = request.json
	#text_result = text_total["result"]
	#text_pa = text_result["parameters"]
	text_un = text_pa["dni"]
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/alias/?dni='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["properties"]
	respuesta_re = respuesta_pro["resenas"]
	respuesta_item = respuesta_re["items"]
	respuesta_img = respuesta_item["ref"]
	final = "La url de la imagen con dni "+text_un+" es " +respuesta_img
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")

@app.route('/auxilio', methods=["POST"])
def crear_auxilio():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["dni"]
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "Registrado auxilio"
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")

@app.route('/identificacion', methods=["POST"])
def crear_identificacion():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["dni"]
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "Registrada identificacion"
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")

@app.route('/avistamiento', methods=["POST"])
def crear_avistamiento():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["matricula"]
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://104.154.101.83/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "Registrado avistamiento"
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")


if __name__ == "__main__":
	app.run()

	
