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
	"""
	respuesta_modelo = respuesta_pro[0]["modelo"]
	respuesta_marca1 = respuesta_pro[0]["marca"]
	respuesta_marca = respuesta_marca1["descripcionLarga"]
	respuesta_bastidor = respuesta_pro[0]["numeroBastidor"]
	respuesta_color1 = respuesta_pro[0]["colorPrimario"]
	respuesta_color = respuesta_color1["descripcionLarga"]
	respuesta_matricula = respuesta_pro[0]["matricula"]
	
	respuesta_modelo2 = respuesta_pro[1]["modelo"]
	respuesta_marca21 = respuesta_pro[1]["marca"]
	respuesta_marca2 = respuesta_marca21["descripcionLarga"]
	respuesta_bastidor2 = respuesta_pro[1]["numeroBastidor"]
	respuesta_color21 = respuesta_pro[1]["colorPrimario"]
	respuesta_color2 = respuesta_color21["descripcionLarga"]
	respuesta_matricula2 = respuesta_pro[1]["matricula"]
	
	final = "El vehículo con matricula "+respuesta_matricula+" es de la marca "+respuesta_marca+" su modelo es "+respuesta_modelo+" de color "+respuesta_color+" y con número de bastidor "+respuesta_bastidor+"."
	final2 = "El vehículo con matricula "+respuesta_matricula2+" es de la marca "+respuesta_marca2+" su modelo es "+respuesta_modelo2+" de color "+respuesta_color2+" y con número de bastidor "+respuesta_bastidor2+"."
	final = final + '\n' + final2
	"""
	for i in respuesta_pro:
		final += "El vehículo con matricula "+i["matricula"]+" es de la marca "+i["marca"]["descripcionLarga"]+" su modelo es "+i["modelo"]+" de color "+i["colorPrimario"]["descripcionLarga"]+" y con número de bastidor "+i["numeroBastidor"]+"."+'\n'
	
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
	url = 'http://35.184.86.19/registro/?id='
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
	url = 'http://35.184.86.19/registro/?id='
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
	url = 'http://35.184.86.19/registro/?id='
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
