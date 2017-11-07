from flask import Flask
import requests
from flask import Response, make_response
from flask import request, jsonify
import json
from flask_assistant import core
from flask_cors import cross_origin, CORS
app = Flask(__name__)
cors = CORS(app)

@app.route('/', methods=['GET', 'POST'])
def index():
	response_index = ""
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_consulta = text_pa["consulta"]
	if text_consulta == "1":
		response_index = persona_preguntar()
	if text_consulta == "2":
		response_index = vehiculo_preguntar()
	if text_consulta == "3":
		response_index = crear_identificacion()
	if text_consulta == "4":
		response_index = crear_avistamiento()
	if text_consulta == "5":
		response_index = crear_auxilio()
	if text_consulta == "6":
		print("Saludo hecho")
		#Aqui con el parametro "saludo", habría que ver si ha hecho una consulta, y coger el dni o matricula
		
	return response_index

@app.route('/vehiculos', methods=["POST"])
def vehiculo_preguntar():
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["matricula"]
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.184.86.19/vehiculos/?matricula='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["properties"]
	final = ""
	for i in respuesta_pro:
		final += "Matricula "+i["matricula"]+" Marca "+i["marca"]["descripcionLarga"]+" Modelo "+i["modelo"]+" Color "+i["colorPrimario"]["descripcionLarga"]+ " Tipo "+i["tipo"]["title"]+" Bastidor "+i["numeroBastidor"]
	
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
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
	url = 'http://35.184.86.19/alias/?dni='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	print(datajson)
	respuesta_pro = datajson["properties"]
	#Nombre
	respuesta_nombre = respuesta_pro["nombreCompleto"]["properties"]["nombre"]["title"]
	#Primer Apellido
	respuesta_primerApellido = respuesta_pro["nombreCompleto"]["properties"]["primerApellido"]["title"]
	#Segundo Apellido
	respuesta_segundoApellido = respuesta_pro["nombreCompleto"]["properties"]["segundoApellido"]["title"]
	#Fecha Nacimiento
	respuesta_fechaNacimiento = respuesta_pro["fechaNacimiento"]["properties"]["fecha"]["title"]
	#URL DNI
	respuesta_re = respuesta_pro["resenas"]
	respuesta_item = respuesta_re["items"]
	respuesta_img = respuesta_item["ref"]
	final = "Nombre "+respuesta_nombre+" Primer "+respuesta_primerApellido+" Segundo "+respuesta_segundoApellido+" Fecha "+repuesta_fechaNacimiento+" URL "+respuesta_fechaNacimiento
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
	url = 'http://35.184.86.19/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "200"
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
	url = 'http://35.184.86.19/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "200"
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
	url = 'http://35.184.86.19/registro/?id='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["respuesta"]
	final = "200"
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")


if __name__ == "__main__":
	app.run()
