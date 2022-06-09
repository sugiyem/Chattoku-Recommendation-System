import pickle
import warnings
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify

warnings.simplefilter("ignore", FutureWarning)

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

genre_lists = ['Action', 'Adventure', 'Drama', 'Fantasy', 'Comedy', 'Sci-Fi', 'Suspense',
               'Romance', 'Slice of Life', 'Supernatural', 'Mystery', 'Award Winning',
               'Sports', 'Ecchi', 'Avant Garde', 'Horror', 'Boys Love', 'Gourmet',
               'Girls Love', 'Military', 'Childcare', 'Gore', 'Survival', 'Psychological',
               'Time Travel', 'Gag Humor', 'Historical', 'Parody', 'Samurai', 'Adult Cast',
               'Space', 'Romantic Subtext', 'School', 'Iyashikei', 'Strategy Game', 'Mecha',
               'Super Power', 'Vampire', 'Mythology', 'Team Sports', 'Isekai',
               'Reincarnation', 'Anthropomorphic', 'Love Polygon', 'Performing Arts',
               'Combat Sports', 'Martial Arts', 'Delinquents', 'Workplace', 'Music',
               'Organized Crime', 'Otaku Culture', 'CGDCT', 'Showbiz', 'Detective',
               'Visual Arts', 'Harem', 'Mahou Shoujo', 'Racing', 'High Stakes Game',
               'Video Game', 'Idols (Male)', 'Idols (Female)', 'Crossdressing',
               'Reverse Harem', 'Medical', 'Pets', 'Magical Sex Shift', 'Educational',
               'Josei', 'Kids', 'Seinen', 'Shoujo', 'Shounen']

anime_data = pd.read_csv("./dataset/mal_top2000_anime.csv",
                         usecols=["Name", "Score", "Genres", "Theme(s)", "Demographic"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():
    input = request.get_json(force=True)
    genres = input['genres'].split(", ")

    print(genres)

    array_genres = pd.Series(0, index=genre_lists)

    for genre in set(genres).intersection(genre_lists):
        array_genres.loc[genre] = 1

    final_genres = np.array([array_genres.values])
    print(final_genres)

    target_index = model.kneighbors(final_genres, return_distance=False)
    print(target_index)

    result = anime_data.loc[anime_data.index[target_index][0]]
    json_result = {
        "result": result.Name.astype(str).values.tolist()
    }

    return jsonify(json_result)


if __name__ == "__main__":
    app.run(debug=True)
