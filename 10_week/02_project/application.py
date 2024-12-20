from flask import Flask, render_template, request, session
from requests import Session
import src.utils as su

import recommender as rc
import src.viz as viz

# sess = Session()

app = Flask(__name__)
# @app.route('/', methods=['GET', 'POST'])
# def index():



#     # method_pred = None

#     # if request.args.getlist("method")[0]



#     return render_template('index.html', movies = rc.movies['title'], method_pred = None)

@app.route('/', methods = ['GET', 'POST'])
def index():

    method_pred = 'most_popular'
    if request.args.getlist("rec_method"):
        method_pred = request.args.getlist("rec_method")[0]

    print(method_pred)

    session['method_pred'] = method_pred

    render = render_template(
        'index.html',
        movies = rc.movies['title'], 
        method_pred = method_pred)
      


    return render


@app.route('/recommender/', methods = ['GET'])
def recommender():

    method_pred = session['method_pred']

    movie_names = request.args.getlist("title")
    movie_ids = [su.get_id(mov, movies = rc.movies) for mov in movie_names]

    movie_ratings = [int(x) for x in request.args.getlist("rating")]

    k_recs = int(request.args.getlist("kpred")[0])

    query = {}

    movrec = rc.MovieRecommender(
        user_ratings=rc.ratings,
        movies=rc.movies
    )



    

    if(method_pred == 'NFM'):
    
        query = su.make_query_list(movie_ids, movie_ratings)

    
    recs = movrec.recommend(
        query = query,
        method = method_pred, 
        k = k_recs, 
        model = rc.MODEL_PATH)
    recs = su.get_movie(id = recs.columns, movie_df = rc.movies)

    return render_template('recommender.html', recs = recs)


@app.route('/dbexplore/', methods = ['GET', 'POST'])
def dbex():




    render = render_template(
        'db_explore.html',
        )
      
    return render


@app.route('/api/data/')
def data():



    print(rc.movies.head())
    data_dict = {'data' : [r.to_dict() for i,r in rc.movies.reset_index().iterrows()]}
    print(data_dict['data'][0])

    return data_dict

@app.route('/dbmovies/')
def dbmovies():

    return render_template("db_movies.html")

@app.route('/dbusers/')
def dbusers():

    plot = viz.plot_users()

    return render_template("db_users.html", plot = plot)



if __name__ == '__main__':
    # print(rc.movies.head())
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    # sess.init_app(app)
    app.run(debug=True)
    
