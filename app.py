from flask import Flask, render_template, request
import pickle
import requests
import pandas as pd
import joblib

app = Flask(__name__)

# Api Funkcijos
def fetch_poster(movie_id):
    api_key = "c7ec19ffdd3279641fb606d19ceb9bb1"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    if response.status_code != 200:
        return "posteris nerastas"
    data = response.json()
    return f"https://image.tmdb.org/t/p/w500/{data.get('poster_path', '')}"

def fetch_trailer(movie_id):
    api_key = "c7ec19ffdd3279641fb606d19ceb9bb1"
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US&api_key={api_key}"
    response = requests.get(url)
    if response.status_code != 200:
        return "treileris nerastas"
    data = response.json()

    for video in data.get("results", []):
        if video.get("type") == "Trailer" and video.get("site") == "YouTube":
            return f"https://www.youtube.com/watch?v={video['key']}"

    return "treileris nerastas"

# Duomenų įkelimas
movies = pickle.load(open("movies_list.pkl", 'rb'))
movies_info = pickle.load(open("movies_info.pkl", 'rb'))
movies_list = movies['title'].values

# Ленивая загрузка similarity.pkl
similarity = None

def load_similarity():
    global similarity
    if similarity is None:
        similarity = pickle.load(open("similarity.pkl", 'rb'))
    return similarity

# Рекомендации
def recommend(movie):
    # Загружаем similarity при необходимости
    similarity_matrix =  joblib.load("similarity.pkl")
    
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity_matrix[index])), key=lambda x: x[1], reverse=True)[1:6]

    recommended_data = {
        "titles": [],
        "posters": [],
        "vote_averages": [],
        "languages": [],
        "overviews": [],
        "genres": [],
        "dates": [],
        "vote_counts": [],
        "trailers": []
    }

    for i in distances:
        idx = i[0]
        movie_id = movies.iloc[idx].id
        info = movies_info.iloc[idx]

        recommended_data["titles"].append(movies.iloc[idx].title)
        recommended_data["posters"].append(fetch_poster(movie_id))
        recommended_data["vote_averages"].append(info.vote_average)
        recommended_data["languages"].append(info.original_language)
        recommended_data["overviews"].append(info.overview)
        recommended_data["genres"].append(info.genre)
        recommended_data["dates"].append(info.release_date)
        recommended_data["vote_counts"].append(info.vote_count)
        recommended_data["trailers"].append(fetch_trailer(movie_id))

    return recommended_data

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/find', methods=["GET", "POST"])
def find():
    selected_data = {
        "movie": None,
        "poster": None,
        "average": None,
        "language": None,
        "overview": None,
        "genre": None,
        "date": None,
        "vote_count": None,
        "trailer": None
    }

    recommended_data = {
        "titles": [],
        "posters": [],
        "vote_averages": [],
        "languages": [],
        "overviews": [],
        "genres": [],
        "dates": [],
        "vote_counts": [],
        "trailers": []
    }

    if request.method == "POST":
        selected_movie = request.form.get("movie")
        if selected_movie:
            index = movies[movies['title'] == selected_movie].index[0]
            movie_id = movies.iloc[index].id
            info = movies_info.iloc[index]

            selected_data.update({
                "movie": selected_movie,
                "poster": fetch_poster(movie_id),
                "average": info.vote_average,
                "language": info.original_language,
                "overview": info.overview,
                "genre": info.genre,
                "date": info.release_date,
                "vote_count": info.vote_count,
                "trailer": fetch_trailer(movie_id)
            })

            recommended_data = recommend(selected_movie)

    return render_template("find.html",
                           movies_list=movies_list,
                           zip=zip,
                           selected_movie=selected_data["movie"],
                           selected_poster=selected_data["poster"],
                           selected_avarage=selected_data["average"],
                           selected_origina_language=selected_data["language"],
                           selected_overwiev=selected_data["overview"],
                           selected_genres=selected_data["genre"],
                           selected_date=selected_data["date"],
                           selected_vote_count=selected_data["vote_count"],
                           selected_trailer=selected_data["trailer"],

                           recommended_movies=recommended_data["titles"],
                           recommended_posters=recommended_data["posters"],
                           recommend_vote_avarages=recommended_data["vote_averages"],
                           recommend_original_languages=recommended_data["languages"],
                           recommend_overviews=recommended_data["overviews"],
                           recommend_genres=recommended_data["genres"],
                           recommend_dates=recommended_data["dates"],
                           recommend_vote_counts=recommended_data["vote_counts"],
                           recommend_trailers=recommended_data["trailers"])

if __name__ == "__main__":
    app.run(debug=True)
