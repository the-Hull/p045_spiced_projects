from flask import Flask, render_template, request
import src.utils as su
import recommender as rc

app = Flask(__name__)
# @app.route('/', methods=['GET', 'POST'])
# def index():



#     # method_pred = None

#     # if request.args.getlist("method")[0]



#     return render_template('index.html', movies = rc.movies['title'], method_pred = None)

@app.route('/', methods = ['GET', 'POST'])
def index():

    method_pred = None
    if request.args.getlist("rec_method"):
        method_pred = request.args.getlist("rec_method")[0]

    print(method_pred)
    render = render_template(
        'index.html',
        movies = rc.movies['title'], 
        method_pred = method_pred)
      


    return render


@app.route('/recommender/')
def recommender():
    return render_template('recommender.html')
if __name__ == '__main__':
    print(rc.movies.head())
    app.run(debug=True)
    
