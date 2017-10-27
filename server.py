from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse

from flask import Flask, request, Response, render_template, send_from_directory
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_url_path="")
cors = CORS(app)

@app.route("/selenium/", methods=["GET"])
def selenium():
	driver = webdriver.PhantomJS()
	endpoint = "FashionWeek"
	url = "https://twitter.com/"
	url_final = url + endpoint
	driver.get(url_final)
	driver.implicitly_wait(10)
	lista_tweets = driver.find_elements_by_tag_name('p')
	tweets = ""
	for tweet in lista_tweets:
		tweets += tweet.text
	print(tweets)
	return tweets

@app.route("/", methods=["GET"])
def hola():
	print("hola")
	
if __name__ == '__main__':
	app.run("0.0.0.0", 80)
	print("hola")
	selenium()
	

	
