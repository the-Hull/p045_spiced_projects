import tweepy
import os
import logging
import utils

mongo_db = utils.extract()

print('here')
print(mongo_db)
tweet_scores = utils.transform(mongo_db, 'tweets') 
utils.load(tweet_scores)