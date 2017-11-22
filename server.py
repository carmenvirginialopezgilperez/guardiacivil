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
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_consulta = text_pa["consulta"]
	if text_consulta == "1":
		return persona_preguntar()
	if text_consulta == "2":
		return vehiculo_preguntar()
	if text_consulta == "3":
		return crear_identificacion()
	if text_consulta == "4":
		return crear_avistamiento()
	if text_consulta == "5":
		return crear_auxilio()
	if text_consulta == "6":
		info = ""
		tipoAlta = ""
		cont = 0
		matOrDni = text_pa["peticionSaludo"]
		text_query = text_result["resolvedQuery"]
		text_peticion = text_pa["peticion"]
		for i in text_query:
			if i == " ":
				if info == "avistamiento" or info == "identificacion" or info == "identificación" or info == "auxilio":
					tipoAlta = info
				if not((cont > 0) and (text_query[cont-1] == 0 or text_query[cont-1] == 1 or text_query[cont-1] == 2 or text_query[cont-1] == 3 or text_query[cont-1] == 4 or text_query[cont-1] == 5 or text_query[cont-1] == 6 or text_query[cont-1] == 7 or text_query[cont-1] == 8 or text_query[cont-1] == 9)):
					info = ""
			else:
				info += i
			cont += 1
		print(text_peticion+", "+tipoAlta+", "+matOrDni+", "+info)
		
		if text_peticion == "Alta":
			if  tipoAlta == "avistamiento":
				response_index = crear_avistamiento2(info)
			if  tipoAlta == "identificacion" or tipoAlta == "identificación":
				response_index = crear_identificacion2(info)
			if  tipoAlta == "auxilio":
				response_index = crear_auxilio2(info)
		if text_peticion == "Consulta":
			if matOrDni == "dni" or matOrDni == "DNI" or matOrDni == "Dni":
				response_index = persona_preguntar2(info)
			if matOrDni == "matricula" or matOrDni == "Matricula" or matOrDni == "Matrícula" or matOrDni == "matrícula":
				response_index = vehiculo_preguntar2(info)
		if matOrDni != "":
			return response_index
		else:
			final = "0"
			final_texto = {"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
			json_data_final = json.dumps(final_texto)
			return Response(json_data_final, status=200, mimetype="application/json")
		

@app.route('/vehiculos', methods=["POST"])
def vehiculo_preguntar():
	
	text_total = request.json
	text_result = text_total["result"]
	text_pa = text_result["parameters"]
	text_un = text_pa["matricula"]
	if text_un ==  "Consulta vehiculo":
		final_texto = "errorV"
		json_data_final = json.dumps(final_texto)
		return Response(json_data_final, status=200, mimetype="application/json")
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/vehiculos/?matricula='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["properties"]
	final = "vehiculoconsulta¬"
	for i in respuesta_pro:
		final += i["matricula"]+"¬"+i["marca"]["descripcionLarga"]+"¬"+i["modelo"]+"¬"+i["colorPrimario"]["descripcionLarga"]+ "¬"+i["tipo"]["title"]+"¬"+i["numeroBastidor"]
		final += "¡"
	final = final[:-1]
	print(final)
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
	url = 'http://35.202.165.151/alias/?dni='
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
	##URL DNI
	respuesta_re = respuesta_pro["resenas"]
	respuesta_item = respuesta_re["items"]
	respuesta_img = respuesta_item["ref"]
	final = "personaconsulta¬"+respuesta_nombre+"¬"+respuesta_primerApellido+"¬"+respuesta_segundoApellido+"¬"+respuesta_fechaNacimiento+"¬"+respuesta_img
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
	url = 'http://35.202.165.151/registro/?id='
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
	url = 'http://35.202.165.151/registro/?id='
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
	url = 'http://35.202.165.151/registro/?id='
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

###################
@app.route('/vehiculos', methods=["POST"])
def vehiculo_preguntar2(matricula):
	text_un = matricula
	data = {}
	data['matricula'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/vehiculos/?matricula='
	url_final = url + text_un
	respuesta = requests.get(url_final).content
	s = requests.session()
	s.keep_alive = False
	my_json = respuesta.decode('utf8').replace("'", '"')
	datajson = json.loads(my_json)
	respuesta_pro = datajson["properties"]
	final = ""
	for i in respuesta_pro:
		final += i["matricula"]+"$"+i["marca"]["descripcionLarga"]+"$"+i["modelo"]+"$"+i["colorPrimario"]["descripcionLarga"]+ "$"+i["tipo"]["title"]+"$"+i["numeroBastidor"]
		final += "*"
	final = final[:-1]
	print(final)
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")


@app.route('/alias', methods=["POST"])
def persona_preguntar2(dni):
	text_un = dni
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/alias/?dni='
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
	final = respuesta_nombre+"$"+respuesta_primerApellido+"$"+respuesta_segundoApellido+"$"+respuesta_fechaNacimiento+"$"+respuesta_img
	final_texto={"speech":final,"displayText":final,"data":{},"contextOut":[],"source":"webhook"}
	json_data_final = json.dumps(final_texto)
	return Response(json_data_final, status=200, mimetype="application/json")

@app.route('/auxilio', methods=["POST"])
def crear_auxilio2(dni):
	text_un = dni
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/registro/?id='
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
def crear_identificacion2(dni):
	text_un = dni
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/registro/?id='
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
def crear_avistamiento2(matricula):
	text_un = matricula
	data = {}
	data['dni'] = text_un
	json_data = json.dumps(data)
	url = 'http://35.202.165.151/registro/?id='
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
###################


if __name__ == "__main__":
	app.run()
