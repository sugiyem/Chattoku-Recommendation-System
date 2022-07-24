import numpy as np
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors


anime_data = pd.read_csv("./dataset/mal_top3000.csv", index_col="Mal_id")

# print(anime_data.info())
# print(anime_data.head())

processed_anime_data = anime_data.copy()

genres = processed_anime_data.Genres.str.strip(
    "[]").str.replace("'", "").str.split(",", expand=True)
unique_genres = pd.Series(genres.values.ravel()).dropna().unique()
unique_genres = unique_genres[unique_genres != ""]

# print(len(unique_genres))
# print(unique_genres)

dummy_genres = pd.get_dummies(genres)

for genre in unique_genres:
    processed_anime_data[genre] = dummy_genres.loc[:,
                                                   dummy_genres.columns.str.endswith(genre)].sum(axis=1)

# print(processed_anime_data.head())

themes = processed_anime_data.Themes.str.strip(
    "[]").str.replace("'", "").str.split(",", expand=True)
unique_themes = pd.Series(themes.values.ravel()).dropna().unique()
unique_themes = unique_themes[unique_themes != ""]

# print(len(unique_themes))
# print(unique_themes)

dummy_themes = pd.get_dummies(themes)

for theme in unique_themes:
    processed_anime_data[theme] = dummy_themes.loc[:,
                                                   dummy_themes.columns.str.endswith(theme)].sum(axis=1)

# print(processed_anime_data.head())

demographics = processed_anime_data.Demographics.str.strip(
    "[]").str.replace("'", "").str.split(",", expand=True)
unique_demographics = pd.Series(demographics.values.ravel()).dropna().unique()
unique_demographics = unique_demographics[unique_demographics != ""]

# print(len(unique_demographics))
# print(unique_demographics)

dummy_demos = pd.get_dummies(demographics)

for demographic in unique_demographics:
    processed_anime_data[demographic] = dummy_demos.loc[:,
                                                        dummy_demos.columns.str.endswith(demographic)].sum(axis=1)

processed_anime_data = processed_anime_data.drop(
    columns=["Score", "Genres", "Themes", "Demographics"])

# print(processed_anime_data.shape[1])
# print(processed_anime_data.head())

genre_lists = np.append(unique_genres, np.append(
    unique_themes, unique_demographics))

# print(len(genre_lists))
# print(genre_lists)

knn_model = NearestNeighbors(n_neighbors=10)
knn_model.fit(processed_anime_data.values)

file = open("model.pkl", "wb")
pickle.dump(knn_model, file)
file.close()
