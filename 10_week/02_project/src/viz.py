import pandas as pd
import utils as su

movies = pd.read_csv('../00_data/ml-latest-small/movies.csv', index_col='movieId')
# ratings = su.prep_ratings("../00_data/nmf_ratings_matrix.json", 0)


if __name__ == "__main__":
    subs = movies.iloc[:10, ]
    

    for i, r in subs.reset_index().iterrows():
        print(r.to_dict())
