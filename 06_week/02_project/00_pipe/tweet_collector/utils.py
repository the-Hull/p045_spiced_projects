import tweepy
import re
import pandas as pd


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
    return re.sub('(https[\W\w:/.]+[\n]?)', '', data)
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


