import src.utils as su
import pandas as pd



# CONSTS
MODEL_PATH = "../00_models/nmf.bin"

# load data
# movies = pd.read_csv('../00_data/ml-latest-small/movies.csv', index_col='movieId')
# movies['year'] = movies.title.str.extract("[(](\d{4})[)]")
ratings = su.prep_ratings("../00_data/nmf_ratings_matrix.json", 0)





movies = pd.read_json("../00_data/movie_ratings.json").set_index('movieId')
movies.fillna(value=0000, inplace=True)

class MovieRecommender:

    def __init__(self, user_ratings, movies):
        
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
            assert 'query' in self.__dict__.keys(), "Need argument `query` with a query in recommend() for method NFM"
            
            self.recommendation = su.recommend_nmf(
                query = self.query,
                user_ratings=self.user_ratings,
                movies=self.movies,
                model = self.model,
                k = self.k)

        elif self.method == 'most_popular':
            self.recommendation = su.recommend_most_popular(
                user_ratings=self.user_ratings,
                movies=self.movies,
                k = self.k)
        else:
            raise ValueError(f'method must be NFM or most_popular')

        return self.recommendation

if __name__ == "__main__":

    print(movies.columns)
    print(movies.head())
    
    # print(su.get_id('Black Butler: Book of the Atlantic (2017)', movies = movies))
    # print(type(su.get_id('Black Butler: Book of the Atlantic (2017)', movies = movies)))

    # movrec = MovieRecommender(
    #     user_ratings=ratings,
    #     movies=movies
    # )

    # movrec.recommend(
    #     query = {1:5, 2:5, 3:2.5, 356: 4, 480: 2, 260: 5, 12: 4, 300: 1},
    #     method = 'NFM', 
    #     k = 1, 
    #     model = MODEL_PATH) # must work
    # movrec.recommend(method = 'NFM', k = 3) # must fail
    # movrec.recommend(method = 'most_popluar', k = 5) # must work
