# Andrea Estefania Elias Cobar
# Api request test
# se debe de obtener 25 jokes diferentes (verificar que el contenido sea distinto)

from flask import Flask, jsonify
import requests

app = Flask(__name__)

#ruta
@app.route('/api/chucknorris', methods=['GET'])

## Definimos la funcion para hacer el get al api chuck norris

def get_chucknorris_jokes():

     #arrays para guardar los datos obtenidos del GET
    
    jokes = []
    ids = set()  # Conjunto para evitar duplicados de ID

 #Vemos que tengamos menos de 25 jokes en el array, se dice menor a 25 ya que se comienza desde 0.
    while len(jokes) < 25:
        response = requests.get('https://api.chucknorris.io/jokes/random')
        joke = response.json()

 # verificamos que el id no se encuentre ya dentro del array previamente definido
        if joke['id'] not in ids:
            joke_data = {
                'id': joke['id'],
                'joke': joke['value']
            }
            jokes.append(joke_data)
            ids.add(joke['id'])

            

    return jsonify(jokes)

if __name__ == '__main__':
    app.run()
