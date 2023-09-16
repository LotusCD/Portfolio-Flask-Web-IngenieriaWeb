import os
from flask import Flask, render_template
from flask_pymongo import PyMongo
from database import manage_database
from flask_caching import Cache


app = Flask(__name__)

# MongoDB connection string (update with your credentials)
# Agregar desde linea de comando, por ejemplo: export DB_USERNAME=db_iudigital

username = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')

if not username or not password:
    raise EnvironmentError("Database credentials not set!")

#app.config["MONGO_URI"] = "mongodb://localhost:27017/peliculas_iu_db"
app.config["MONGO_URI"] = f'mongodb+srv://{username}:{password}@cluster0.e3m56i8.mongodb.net/sample_mflix?retryWrites=true&w=majority'

# Caching configuration
cache_config = {
    "DEBUG": True,           # some Flask specific configs
    "CACHE_TYPE": "simple",  # Can be "memcached", "redis", etc.
    "CACHE_DEFAULT_TIMEOUT": 3600  # Cache timeout in seconds
}
app.config.from_mapping(cache_config)
cache = Cache(app)

mongo = PyMongo(app)

#Dejando esto fuera ya que de momento usaremos solo los datasets de muestra de Mongo
#manage_database(mongo)

#Llamamos la colección de nuestro interes, esto es lo que vamos a pasar para renderizar nuestros templates
collection_names = mongo.db.list_collections_names
movie_collection = mongo.db.movies

@app.route('/')
def index():
    try:
        peliculas = movie_collection.find({"year": {"$gt": 2014}}).limit(20)
        return render_template('index.html', peliculas=peliculas)
    except Exception as e:
        return str(e)

@app.route('/genero/')
def genero():
    try:
        genres = ["Adventure", "Horror", "Sci-Fi", "Romance"] # Add more genres as needed
        genre_movies = {}
        for genre in genres:
            # Fetch movies belonging to the given genre and limit them for display (for example, top 10)
            peliculas = movie_collection.find({"genres": genre, "year": {"$gt": 2014}}).limit(10)
            genre_movies[genre] = peliculas
        return render_template('genero.html', genre_movies=genre_movies)
    except Exception as e:
        return str(e)


@app.route('/director/')
def director():
    # Fetch data from the database and create the 'director_movies' dictionary.
    # For example:
    director_movies = {}
    try:
        all_movies = movie_collection.find({"year": {"$gt": 2014}}).limit(20)
        for movie in all_movies:
            for director in movie['directors']:
                if director not in director_movies:
                    director_movies[director] = []
                director_movies[director].append(movie)

        # Render the template and pass the dictionary.
        return render_template('director.html', director_movies=director_movies)



    except Exception as e:
        return str(e)



if __name__ == "__main__":
    app.run(debug=True)

