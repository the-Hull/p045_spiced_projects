import tweepy
import os
# Here we need to import our credentials:
# from credentials_anastasia import BEARER_TOKEN
import logging


from datetime import datetime

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
logging.critical("\n" + current_time)


BEARER_TOKEN = os.getenv("TWITTER_BEARER")


print(BEARER_TOKEN[1:5])

client = tweepy.Client(bearer_token=BEARER_TOKEN)

if client:
    logging.critical("\nAuthentication OK")
else:
    logging.critical('\nVerify your credentials')


safiyanoble = client.get_user(username='safiyanoble', user_fields=['name', 'id', 'created_at'])
user = safiyanoble.data

logging.log(level=1, 
    msg = f'The user with name {user.name} and ID {user.id} created their twitter account on {user.created_at}')

print(f'The user with name {user.name} and ID {user.id} created their twitter account on {user.created_at}' )
