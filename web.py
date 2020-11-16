from flask import Flask
from flask import render_template
from flask import request
import redis
import json

app = Flask(__name__)

r = redis.Redis(host='localhost', port=6379, db=0)
with open('ratings.json') as data_file:
    test_data = json.load(data_file)
    for x in test_data:
        r.set(str(x['Title']), str(x['IMDB_Rating']))


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/", methods=['POST'])
def crudops():
    movie = request.form['movietitle']
    rating = r.get(movie)
    value = request.form['call']
    formrating = request.form['ratingimdb']
    if value == 'create':
        if rating is not None:
            formatted = ("Movie name: ", movie , "already exists!")
            return render_template('index.html', message = formatted)
        else:
            r.set(movie, formrating)
            formatted = ("Movie title: ", movie , "Rating: ", formrating, ". entry added successfully.")
            return render_template('index.html', message = formatted)

    if value == 'update':
        if rating is not None:
            r.set(movie, formrating)
            formatted = ("Movie title: ", movie , "Rating: ", formrating, ". entry updated successfully.")
            return render_template('index.html', message = formatted)
        else:
            if rating is None:
                formatted = ("You cannot update this entry because it does not exist.")
                return render_template('index.html', message = formatted)

    if value == 'search':
        if rating is not None:
            formatted = ("Movie name: ", movie , "Rating: ", rating)
            return render_template('index.html', message = formatted)
        else:
            formatted = ("Movie name: ", movie , "is not found.")
            return render_template('index.html', message = formatted)

    if value == 'delete':
        if rating is not None:
            r.delete(movie, rating)
            formatted = ("Movie title: ", movie , "Rating: ", rating, ". entry deleted successfully.")
            return render_template('index.html', message = formatted)


if __name__ == "__main__":
    app.run()

