import pandas as pd
from sklearn.impute import SimpleImputer
import pickle
import numpy as np



def prep_ratings(path_json, imputer_fill):
    ratings = pd.read_json(path_json)
    imputer = SimpleImputer(strategy="constant", fill_value=imputer_fill)
    ratings = pd.DataFrame(imputer.fit_transform(ratings), index =ratings.index, columns =ratings.columns)
    return ratings
    


def get_movie(id: int, movie_df: str) -> str :
    """
    Requires movie df with index set movie id
    """
    return movie_df.loc[id, 'title']



def recommend_nmf(query, user_ratings, movies, model, k=10):
    """
    Filters and recommends the top k movies for any given input query based on a trained NMF model. 
    Returns a list of k movie ids.
    """

    # load model 
    model  = pickle.load(open(model, 'rb'))

    # check if queried films exist
    movie_col_idxs = [int(k) for k in query.keys()]
    if not all(x in movies.index.values for x in movie_col_idxs):
        raise ValueError("movie doesn't exist")




    # 1. candiate generation
    # construct a user vector
    user_mat = user_ratings.copy()
    user_mat = user_mat.iloc[[0],:]
    user_mat.iloc[0,:] = 0

    user_mat.loc[:, movie_col_idxs] = [int(v) for v in query.values()]

    # print(user_mat.loc[:, movie_col_idxs])
    # print(user_mat.iloc[:,0:10 ])

      
    # 2. scoring
    # calculate the score with the NMF model
    user_scoring = model.transform(user_mat)
    
    # 3. ranking
    user_ranking = np.dot(user_scoring, model.components_)

    # update
    

    

    user_ranking = pd.DataFrame(data = user_ranking, columns = user_ratings.columns, index = ['user'])
    # set zero score to movies allready seen by the user
    user_ranking.loc[:, movie_col_idxs] = 0



    top_rankings = user_ranking.sort_values(by = 'user', axis = 1, ascending = False).iloc[[0], 0:k]

    # return the top-k highst rated movie ids or titles
    print(get_movie(id = top_rankings.columns, movie_df = movies))


    return top_rankings
