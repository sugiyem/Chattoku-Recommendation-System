import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors


anime_data = pd.read_csv("./dataset/mal_top2000_anime.csv",
                         usecols=["Name", "Score", "Genres", "Theme(s)", "Demographic"])

print(anime_data.info())

cleaned_anime_data = anime_data.copy()
cleaned_anime_data["Theme"] = cleaned_anime_data["Theme(s)"]

genres = cleaned_anime_data.Genres.str.strip(
    "[]").str.replace("'", "").str.split(", ", expand=True)
unique_genres = pd.Series(genres.values.ravel()).dropna().unique()
unique_genres = unique_genres[unique_genres != 'None']

print(len(unique_genres))
print(unique_genres)

dummy_genres = pd.get_dummies(genres)

for genre in unique_genres:
    cleaned_anime_data[genre] = dummy_genres.loc[:,
                                                 dummy_genres.columns.str.endswith(genre)].sum(axis=1)

print(cleaned_anime_data.head())

themes = cleaned_anime_data.Theme.str.strip(
    "[]").str.replace("'", "").str.split(", ", expand=True)
unique_themes = pd.Series(themes.values.ravel()).dropna().unique()
unique_themes = unique_themes[unique_themes != 'None']

print(len(unique_themes))
print(unique_themes)

dummy_themes = pd.get_dummies(themes)

for theme in unique_themes:
    cleaned_anime_data[theme] = dummy_themes.loc[:,
                                                 dummy_themes.columns.str.endswith(theme)].sum(axis=1)

print(cleaned_anime_data.head())

demo_dummies = pd.get_dummies(cleaned_anime_data.Demographic)

cleaned_anime_data = pd.concat([cleaned_anime_data, demo_dummies], axis=1)
cleaned_anime_data = cleaned_anime_data.drop(
    columns=["Name", "Score", "Genres", "Theme(s)", "Demographic", "Theme", "None"])

print(cleaned_anime_data.shape[1])
print(cleaned_anime_data.head())

knn_model = NearestNeighbors(n_neighbors=5)
knn_model.fit(cleaned_anime_data.values)


def get_details(anime_name):
    return cleaned_anime_data.loc[anime_data[anime_data.Name == anime_name].index].values


def get_anime_recommendations_from_name(anime_name):
    anime_details = get_details(anime_name)
    target_index = knn_model.kneighbors(anime_details, return_distance=False)
    print(target_index)

    return anime_data.loc[anime_data.index[target_index][0]]


#print(get_anime_recommendations_from_name("Spy x Family"))

file = open("model.pkl", "wb")
pickle.dump(knn_model, file)
file.close()
