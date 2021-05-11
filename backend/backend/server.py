from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)    

film_ratings = []

recomendations = []

@app.route("/")
def index():
    return "It's home page, here is nothing to see..."

# метод запроса фильмов и рейтингов
@app.route("/recomendations", methods=['POST']) 
def set_film_ratings():
    user_ratings = request.json
    film_ratings.append(user_ratings)
    return jsonify(film_ratings)

# метод возврата клиенту рекомендаццй
@app.route("/recomendations", methods=['GET'])
def get_recomendations():
    # здесь вызов воркера и загрузка данных в recomendations
    return jsonify(recomendations)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')