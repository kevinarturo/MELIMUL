from flask import Flask, request
import requests
from os import environ
import json

client_id = environ.get('CLIENT_ID')
client_secret = environ.get('CLIENT_SECRET')

port = environ.get('TOKEN_SERVICE_PORT')

app = Flask("FlaskApp")

@app.route('/', methods=['GET'])
def home():
    url_auth_meli = f"https://auth.mercadolibre.com.mx/authorization?response_type=code&redirect_uri=https://localhost:{port}/code&client_id={client_id}"
    return f"Haz click en el siguiente link para generar el acceso <a href='{url_auth_meli}'> CLICK ME!! </a>"

@app.route("/code", methods=['GET'])
def ChangeCodeForToken():
    if "code" in request.args:
        code = request.args["code"] 
        environ["MELI_SERVICE_CODE"] = code

        url = "https://api.mercadolibre.com/oauth/token"

        payload=f'grant_type=authorization_code&client_id={client_id}&client_secret={client_secret}&code={code}&redirect_uri=https%3A%2F%2Flocalhost%3A5500/code'
        headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        response_token = json.loads(response.text)

        environ["ACCESS_TOKEN"] = response_token["access_token"]
        environ["REFRESH_TOKEN"] = response_token["refresh_token"]

        return "El codigo de mercadolibre se ha guardado exitosamente, podras acceder al token generado por MELI en la siguiente ruta: <a href='https://localhost:5500/token'> ACCESS_TOKEN </a>"
    else:
        return "no code"

@app.route("/token", methods=['GET'])
def GenerateToken():
    return environ["ACCESS_TOKEN"]





app.run(host="0.0.0.0", port=5000, ssl_context='adhoc')





