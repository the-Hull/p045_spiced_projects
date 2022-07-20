import src.utils as su
import pandas as pd



# CONSTS
MODEL_PATH = "../00_models/nmf.bin"

# load data
movies = pd.read_csv('../00_data/ml-latest-small/movies.csv', index_col='movieId')
ratings = su.prep_ratings("../00_data/nmf_ratings_matrix.json", 0)



recommendation = su.recommend_nmf(
    query = {1:5, 2:5, 3:2.5, 356: 4, 480: 2, 260: 5, 12: 4, 300: 1},
    user_ratings=ratings,
    movies=movies,
    model = '../00_models/nmf.bin',
     k = 5)


print(recommendation)