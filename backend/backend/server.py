from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import DataRequired, AnyOf, NumberRange, NoneOf
import pandas as pd
import os
import time
import requests
import json
SECRET_KEY = os.urandom(32)

api_key='53212a91a090db204c77b000662ebc4b'

column_names = ["id", "title", "genres"]
df = pd.read_csv('storage/movies.csv', names=column_names)
all_movies = df.title.to_list()
movies_ratings = []
movies_titles = []
selected_movies = []

app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)

file_movies = open('movies.txt', 'w+')

class MovieForm(FlaskForm):
    mv = StringField('Movie', validators=[DataRequired(), AnyOf(all_movies, "Bad movie, take movie from csv.", None), NoneOf(selected_movies, None, None)])
    rt = FloatField('Rating', validators=[DataRequired(), NumberRange(0, 5, "Bad range")])

class CorrForm(FlaskForm):
    mt = StringField('Correlation method', validators=[DataRequired(), AnyOf(['pearson', 'kendall', 'spearman'], "Bad method, use ‘pearson’, ‘kendall’ or ‘spearman’", None)])



@app.route("/")
def index():
    selected_movies.clear()
    movies_ratings.clear()
    movies_titles.clear()
    if os.path.exists('method.txt'):
        os.remove('method.txt')
    file_movies = open('test.txt', 'w')
    file_movies.close()
    file_movies = open('test.txt', 'w')
    if os.path.exists('res.txt'):
        os.remove('res.txt')
    return render_template('index.html')


@app.route("/movies", methods=['POST', 'GET']) 
def movie_ratings():
    movie = ''
    rating = ''
    mvForm = MovieForm()
    crForm = CorrForm()
    if mvForm.validate_on_submit():
        movie = request.form.get('mv')
        rating = request.form.get('rt')
        file_movies.write(movie + ' ' + rating + '\n')
        movies_titles.append(movie)
        movies_ratings.append(rating)
        selected_movies.append(movie)
    if crForm.validate_on_submit() and len(movies_titles) > 5:
        file_method = open('method.txt', 'w')
        file_method.write(request.form.get('mt'))
        file_method.close()
        file_movies.close()
        return redirect('/recomendations')
    return render_template('movies.html', movies_titles = movies_titles, movies_ratings = movies_ratings, len = len(movies_titles), crForm = crForm, mvForm = mvForm)

@app.route('/recomendations', methods=['POST', 'GET'])
def recs():
    recomendations_links = []
    recomendations_pics  = []
    recomendations_titles = []
    while True:
        time.sleep(3)
        check_file = os.path.exists('res.txt')
        if check_file:
            f = open('res.txt', 'r')
            for i in f:
                rq = requests.get('https://api.themoviedb.org/3/movie/' + i + '?api_key=' + api_key + '&language=en-US')
                if rq.status_code == 200:
                    data = rq.json()
                    title = data['original_title']
                    poster = 'http://image.tmdb.org/t/p/w185' + data['poster_path']
                    link = 'https://www.themoviedb.org/movie/' + i
                    recomendations_links.append(link)
                    recomendations_pics.append(poster)
                    recomendations_titles.append(title)
            return render_template('recomendations.html', recomendations_links = recomendations_links, recomendations_pics = recomendations_pics, recomendations_titles = recomendations_titles , len = len(recomendations_titles), method = request.form.get('mt'))
    
if __name__ == '__main__':
    app.debug = True
    app.run()