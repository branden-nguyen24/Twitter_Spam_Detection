from api_auth import api_auth
# Twitter Developer keys here
# It is CENSORED

def run(api, tweet_ids):
    for tweet_id in tweet_ids:
        try:
            tweet = api.get_status(tweet_id)
            print(tweet.text)
        except Exception as e:
            print(e)

def main():
    api = api_auth()
    tweet_ids = ["329850888376156160", "329850890020331520", "329850889965801474", "329850890905337858", "329850892687908864"]
    run(api, tweet_ids)

if __name__ == "__main__":
    main()