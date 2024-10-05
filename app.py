# Importando a biblioteca Flask
from flask import Flask
# Biblioteca para fazer requisições HTTP
import requests
# Biblioteca para manipulação de JSON
import json
import os

def create_app():
    app = Flask(__name__)

    print(os.environ.get('SECRET_KEY'))

    @app.route('/')
    def home():
        response = requests.get('https://api.artic.edu/api/v1/artworks/search?q=cats')
        data = response.json()

        # O método json.dumps() converte um objeto Python em uma string JSON formatada
        parsed = json.dumps(data, indent=4)
        return parsed
    
    return app