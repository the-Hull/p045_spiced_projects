import src.utils as su
import pandas as pd



# CONSTS
MODEL_PATH = "../00_models/nmf.bin"

# load data
movies = pd.read_csv('../00_data/ml-latest-small/movies.csv', index_col='movieId')
ratings = su.prep_ratings("../00_data/nmf_ratings_matrix.json", 0)


class MovieRecommender:

    def __init__(self, query, user_ratings, movies):
        self.query = query
        self.user_ratings = user_ratings
        self.movies = movies
        # self.k = k

    def __repr__(self) -> str:
        if self.k:
            f'Top {self.k} movie recommendations with the {self.method} method'
        else: 
            f'Top movie recommendations with the {self.method} method'

    def recommend(self, method, k, **kwargs):
        self.method = method
        self.k = k
        self.__dict__.update(kwargs)

        if self.method == 'NFM':

            assert 'model' in self.__dict__.keys(), "Need argument `model` with a model path in recommend() for method NFM"
            self.recommendation = su.recommend_nmf(
                query = self.query,
                user_ratings=self.user_ratings,
                movies=self.movies,
                model = self.model,
                k = self.k)

        if self.method == 'Most Popular':
            self.recommendation = su.recommend_most_popular(
                query = self.query,
                user_ratings=self.user_ratings,
                movies=self.movies,
                k = self.k)









if __name__ == "__main__":
    
    print(su.get_id('Black Butler: Book of the Atlantic (2017)', movies = movies))

    movrec = MovieRecommender(
        query = {1:5, 2:5, 3:2.5, 356: 4, 480: 2, 260: 5, 12: 4, 300: 1},
        user_ratings=ratings,
        movies=movies
    )

    # movrec.recommend(method = 'NFM', k = 3, model = MODEL_PATH) # must work
    movrec.recommend(method = 'NFM', k = 3) # must fail



# recommendation = su.recommend_nmf(
#     query = {1:5, 2:5, 3:2.5, 356: 4, 480: 2, 260: 5, 12: 4, 300: 1},
#     user_ratings=ratings,
#     movies=movies,
#     model = MODEL_PATH,
#      k = 5)


# print(recommendation)


# su.recommend_most_popular(query = {296: 2, 593: 1,589:2, 1:5, 2:5, 3:2.5, 356: 4, 480: 2, 260: 5, 12: 4, 300: 1},
#     user_ratings=ratings,
#     movies=movies,
#     k = 5)


