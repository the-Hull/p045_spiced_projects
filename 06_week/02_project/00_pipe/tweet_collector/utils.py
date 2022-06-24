import tweepy
import re
import pandas as pd
import pymongo
import tweepy
import os
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sqlalchemy import create_engine






def remove_emojis(data):
    # https://stackoverflow.com/a/58356570
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", 
        flags = re.UNICODE)
    return re.sub(emoj, '', data)

def remove_links(data):
    return re.sub('(https[\w:\/.%]+)', '', data)
def remove_linebreaks(data):
    return re.sub('[\n]+', ' ', data)

def clean_tweets(text):
    return remove_linebreaks(remove_links(remove_emojis(text)))

def make_tweet_df(tweet):
    
    tweets = {
        'text': [clean_tweets(tweet.text)],
        'retweets' : [tweet.public_metrics['retweet_count']],
        'likes' : [tweet.public_metrics['like_count']],
        'replies' : [tweet.public_metrics['reply_count']],
        'author_id' : [tweet.author_id],
        'id' : [tweet.id],
        'created_at' : [tweet.created_at]
        }

    return pd.DataFrame(tweets)





### MONGOSTORAGE

def write_to_mongo(df):


    client = pymongo.MongoClient(host="mongodb", port=27017)
    db = client.twitter
    
    
    # Check for duplicate tweet ids
    id_list_dic = list(db.tweets.find({}, {"id": 1, "_id":0}))

    ids_existing = []
    for itm in id_list_dic:
        for k,v in itm.items():
            ids_existing.append(v)

    
    # Grab only matching 


    matches = df['id'].isin(ids_existing)
    

    if all(matches):
        print("no new tweets")
        return db
    elif any(matches):
        print(f"dropping {sum(matches)} duplicate tweets")
        new_idx = [not bool for bool in matches.values]
        df = df[new_idx]
    

            
   
    dc = df.to_dict(orient = 'records')
    


    # n_previous = len(db.tweets.find())

    db.tweets.insert_many(dc)
    print("inserted tweets to db")
  

    return db



def sentiment_analyses(mongo_db, collection_name):


    tweets = mongo_db[collection_name]

    tweet_df = pd.DataFrame(list(tweets.find({})))

    if len(tweet_df.index)<=0:
        raise ValueError("No tweet data found")


    s = SentimentIntensityAnalyzer()

    scores = pd.DataFrame(tweet_df['text'].apply(func= lambda x: s.polarity_scores(x)))

    scores_all = [None] * len(scores)

    for id, sc in enumerate(scores['text']):
        scores_all[id] = sc

    tweet_df = pd.concat(
        [tweet_df, pd.DataFrame(scores_all)],
        axis = 1
        )

    return tweet_df


def write_to_postgres(df):

    print(df.info())

    pg_host = 'postgresdb'
    pg_user = os.getenv('POSTGRES_USER')
    pg_db = os.getenv('POSTGRES_DB')
    pg_pass = os.getenv('POSTGRES_PASSWORD')


    pg = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:5432/{pg_db}', echo=True)

    df.drop(columns = ['_id']).to_sql('tweets', pg, if_exists='replace')

    return True



### Wrappers
def extract():
    

    BEARER_TOKEN = os.getenv("BEARER_TOKEN")

    client = tweepy.Client(bearer_token=BEARER_TOKEN)

    if client:
        logging.critical("\nAuthentication OK")
    else:
        logging.critical('\nVerify your credentials')


    response = client.get_user(
        username='GalaxyKate',
        user_fields=['created_at', 'description', 'location',
                    'public_metrics', 'profile_image_url']
    )

    user = response.data
    cursor = tweepy.Paginator(
        method=client.get_users_tweets,
        max_results = 100,
        id=user.id,
        exclude=['replies', 'retweets'],
        tweet_fields=['author_id', 'created_at', 'public_metrics'],
    ).flatten(limit=200)

    tweetdfs = []
    for tweet in cursor:
                tweetdfs.append(make_tweet_df(tweet))
    tweets = pd.concat(tweetdfs, axis = 0)


    # return mongo db connection
    mongodb = write_to_mongo(tweets)

    return mongodb


def transform(extracted, collection_name):
    return sentiment_analyses(mongo_db=extracted, collection_name=collection_name)

def load(transformed_df):
    return write_to_postgres(df = transformed_df)

    


