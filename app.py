import pickle
import warnings
import numpy as np
import pandas as pd
from flask import Flask, request, render_template, jsonify
from model import genre_lists

warnings.simplefilter("ignore", FutureWarning)

app = Flask(__name__)
model = pickle.load(open("model.pkl", "rb"))

anime_data = pd.read_csv("./dataset/mal_top3000.csv")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=['POST'])
def predict():
    input = request.get_json(force=True)
    genres = input['genres'].split(", ")

    array_genres = pd.Series(0, index=genre_lists)

    for genre in set(genres).intersection(genre_lists):
        array_genres.loc[genre] = 1

    final_genres = np.array([array_genres.values])

    target_index = model.kneighbors(final_genres, return_distance=False)
    # print(target_index)

    result = anime_data.loc[anime_data.index[target_index][0]]
    json_result = {
        "result": result.Mal_id.astype(str).values.tolist()
    }

    return jsonify(json_result)


if __name__ == "__main__":
    app.run(debug=True)
