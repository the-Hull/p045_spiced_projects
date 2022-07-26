import pandas as pd
import json
import plotly
import plotly.express as px


# movies = pd.read_csv('../00_data/ml-latest-small/movies.csv', index_col='movieId')
# ratings = su.prep_ratings("../00_data/nmf_ratings_matrix.json", 0)
ratings = pd.read_csv('../00_data/ml-latest-small/ratings.csv')

def plot_users():
    """
    Generate a Plotly figure and convert it to a JSON string.
    Uses sample data from gapminder as an example.
    """

    data_figure = px.histogram(ratings, x = 'rating',
            labels={'rating':'Rating',
                    'count' : '# Votes'}, # can specify one label per df column
                   opacity=0.8,
                #    log_y=True, # represent bars with log scale
                   color_discrete_sequence=['darkslategray'])

    data_figure.update_layout(
        {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
        })

    data_figure.update_layout(yaxis_title="# Votes")
        
    data_figure.update_xaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')
    data_figure.update_yaxes(showline=True, linewidth=2, linecolor='gray', gridcolor='lightgray')

    data_json = json.dumps(data_figure, cls=plotly.utils.PlotlyJSONEncoder)

    return data_json



if __name__ == "__main__":
    print(ratings.head())

