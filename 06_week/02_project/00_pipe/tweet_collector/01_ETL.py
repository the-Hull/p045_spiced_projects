import tweepy
import os
import logging
import utils

import time

time.sleep(5)  # make sure that ETL can run

mongo_db = utils.extract()
tweet_scores = utils.transform(mongo_db, 'tweets') 
utils.load(tweet_scores)


