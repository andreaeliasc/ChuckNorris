# Andrea Estefania Elias Cobar
# Api request test
# se debe de obtener 25 jokes diferentes (verificar que el contenido sea distinto)

from flask import Flask, jsonify
import asyncio
import aiohttp
import itertools

app = Flask(__name__)

async def fetch_joke(session, ids):
    # Realiza una solicitud GET asincrónica para obtener un chiste aleatorio de Chuck Norris
    async with session.get('https://api.chucknorris.io/jokes/random') as response:
        joke = await response.json()
        # Verifica si el ID del chiste no está en el conjunto de IDs existentes
        if joke['id'] not in ids:
            return joke
        return None

@app.route('/api/chucknorris', methods=['GET'])
async def get_chucknorris_jokes():
    jokes = []  # Lista para almacenar los chistes
    ids = set()  # Conjunto para evitar duplicados de ID

    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in itertools.repeat(None, 25):
            # Crea tareas asincrónicas para obtener los chistes
            task = asyncio.ensure_future(fetch_joke(session, ids))
            tasks.append(task)

        # Ejecuta las tareas asincrónicas de manera concurrente
        joke_responses = await asyncio.gather(*tasks)

        for joke in joke_responses:
            if joke is not None:
                joke_data = {
                    'id': joke['id'],
                    'joke': joke['value']
                }
                jokes.append(joke_data)
                ids.add(joke['id'])

    return jsonify(jokes)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.ensure_future(get_chucknorris_jokes()))
    app.run()
