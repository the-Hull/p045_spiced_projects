from flask import Flask, render_template
import src.utils as su
import recommender as rc

app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html', movies = rc.movies['title'])
@app.route('/recommender/')
def recommender():
    return render_template('recommender.html')
if __name__ == '__main__':
    print(rc.movies.head())
    app.run(debug=True)