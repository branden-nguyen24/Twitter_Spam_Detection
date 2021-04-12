import tweepy
from twitter_token import token  # where the token stored
# Apply for Twitter Developer keys https://developer.twitter.com/
def api_auth():
    # secret key
    api_key = token["api_key"]
    api_key_secret = token["api_key_secret"]
    access_token = token["access_token"]
    access_token_secret = token["access_token_secret"]

    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    # To avoid being blocked 
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    # api = tweepy.API(auth)
    return api