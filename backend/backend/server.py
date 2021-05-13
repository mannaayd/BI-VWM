from flask import Flask, request, jsonify, render_template, redirect
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
import os
SECRET_KEY = os.urandom(32)


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRET_KEY
CORS(app)
if os.path.exists('method.txt'):
    os.remove('method.txt')
if os.path.exists('movies.txt'):
    os.remove('movies.txt')

class MovieForm(FlaskForm):
    mv = StringField('Movie', validators=[DataRequired()])
    rt = StringField('Rating', validators=[DataRequired()])

class CorrForm(FlaskForm):
    mt = StringField('Correlation method', validators=[DataRequired()])



file_movies = open('movies.txt', 'w')
movies = []

@app.route("/")
def index():
    return render_template('index.html')

#@app.route("/movies")
#def movies_():
#    mvForm = MovieForm()
#    crForm = CorrForm()
#    return render_template('movies.html', crForm = crForm, mvForm = mvForm)

# метод запроса фильмов и рейтингов
@app.route("/movies", methods=['POST', 'GET']) 
def movie_ratings():
    movie = None
    rating = None
    mvForm = MovieForm()
    crForm = CorrForm()
    if mvForm.validate_on_submit():
        movie = request.form.get('mv')
        rating = request.form.get('rt')
        file_movies.write(movie + ' ' + rating + '\n')
        movies.append([movie, rating])
    if crForm.validate_on_submit() and len(movies) > 5:
        file_method = open('method.txt', 'w')
        file_method.write(request.form.get('mt'))
        file_method.close()
        file_movies.close()
        return redirect('/recomendations')
    return render_template('movies.html', movies = movies, crForm = crForm, mvForm = mvForm)

if __name__ == '__main__':
    app.debug = True
    app.run()