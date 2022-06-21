import tweepy
import os
import logging
import utils


from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
logging.critical("\n" + current_time)


BEARER_TOKEN = os.getenv("TWITTER_BEARER")



client = tweepy.Client(bearer_token=BEARER_TOKEN)

if client:
    logging.critical("\nAuthentication OK")
else:
    logging.critical('\nVerify your credentials')


########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

response = client.get_user(
    username='GalaxyKate',
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = response.data

print(dict(user))


#########################
# Get a user's timeline #
#########################

# https://docs.tweepy.org/en/stable/pagination.html#tweepy.Paginator
# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

cursor = tweepy.Paginator(
    method=client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics'],

).flatten(limit=20)


tweetdfs = []
for tweet in cursor:
    
    tweetdfs.append(utils.make_tweet_df(tweet))
tweets = utils.pd.concat(tweetdfs, axis = 0)

print(tweets)
print(user.id)    