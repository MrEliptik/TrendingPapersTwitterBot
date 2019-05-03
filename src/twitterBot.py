import tweepy

# Variables that contains the credentials to access Twitter API
ACCESS_TOKEN = 'XXXX'
ACCESS_SECRET = 'XXXX'
CONSUMER_KEY = 'XXXX'
CONSUMER_SECRET = 'XXXX'

class Twitter():

    def __init__(self):
        self.api = self.connect_to_twitter_OAuth()

    # Setup access to API
    def connect_to_twitter_OAuth(self):
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

        api = tweepy.API(auth)
        return api

    def tweet(self, msg):
        self.api.update_status(status = msg)