import pymongo
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

client = pymongo.MongoClient(host="0.0.0.0", port=27017)
db = client.twitter

tweet_df = pd.DataFrame(list(db['tweets'].find({})))

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


