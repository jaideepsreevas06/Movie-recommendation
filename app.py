from flask import Flask, request, render_template
import pickle
import pandas as pd

app = Flask(__name__)

# Load pre-processed data
movies_list = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

@app.route('/', methods=['GET', 'POST'])
def home():
    recommendations = []
    posters = []
    selected_movie = ""
    movie_list = movies_list['Title'].values

    if request.method == 'POST':
        selected_movie = request.form.get('movie_select')
        if selected_movie:
            recommendations, posters = recommend(selected_movie)

    combined = zip(recommendations, posters)  # to pass to Jinja
    return render_template(
    'index.html',
    combined=combined,
    movie_list=movie_list,
    selected_movie=selected_movie,
    recommendations=recommendations  # <-- add this
    )


def recommend(movie):
    try:
        movie_index = movies_list[movies_list['Title'] == movie].index[0]
    except IndexError:
        return [], []

    distances = similarity[movie_index]
    movies_indices = sorted(
        list(enumerate(distances)), reverse=True, key=lambda x: x[1]
    )[1:11]  # Skip the movie itself

    recommended_movies = []
    recommended_posters = []

    for i in movies_indices:
        row = movies_list.iloc[i[0]]
        recommended_movies.append(row['Title'])
        poster = row.get('Poster_Url', 'https://via.placeholder.com/150')  # Fallback
        recommended_posters.append(poster)

    return recommended_movies, recommended_posters

if __name__ == '__main__':
    app.run(debug=True)
