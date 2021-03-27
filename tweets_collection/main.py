from api_auth import api_auth
# Twitter Developer keys here
# It is CENSORED




def run(api, tweet_ids):
    for tweet_id in tweet_ids:
        print("-" * 50)
        try:
            tweet = api.get_status(tweet_id)
            tweet_feature = {
                "tweet": tweet.text,
                "no_followers": tweet.user.followers_count,
                "no_followings": tweet.user.friends_count,
                "no_userfavorites": tweet.user.favourites_count,
                "no_lists": tweet.user.listed_count,
                "no_tweets": tweet.user.statuses_count,
                "no_retweets": tweet.retweet_count,
                "no_favorites": tweet.favorite_count,
                "no_hashtags": len(tweet.entities["hashtags"]),
                "no_usermentions": len(tweet.entities["user_mentions"]),
                "no_urls": len(tweet.entities["urls"]),
            }
            print(tweet_feature)
        except Exception as e:
            print(e)

def main():
    api = api_auth()
    tweet_ids = ["329850888376156160", "329850890020331520", "329850889965801474", "329850890905337858", "329850892687908864"]
    run(api, tweet_ids)

if __name__ == "__main__":
    main()