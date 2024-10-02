# O arquivo _init_.py indica que a pasta é um pacote Python

# Biblioteca para fazer requisições HTTP
import requests
# Biblioteca para manipulação de JSON
import json

response = requests.get('https://api.artic.edu/api/v1/artworks/search?q=cats')
data = response.json()

# O método json.dumps() converte um objeto Python em uma string JSON formatada
parsed = json.dumps(data, indent=4)
print(parsed)