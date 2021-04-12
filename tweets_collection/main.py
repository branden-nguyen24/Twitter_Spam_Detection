from api_auth import api_auth
from twitter_db import parse_file
from tqdm import tqdm
import os.path
import json

def update_tweet(id, tweet_feature, label):
    # parse features of a tweet as a dictionary
    d_tweet = {
        "id": id,
        **tweet_feature,
        "label": label
    }
    return d_tweet

def get_tweet_feature(tweet):
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
    return tweet_feature

    
def output_file(file_path, dict_data):
    # output dict of data as a json file.
    data = []
    try: 
        with open(file_path, "r", encoding='utf-8') as file:
            data = json.load(file)
    except Exception as e:
        print(e)
        print(f"Create a new json file: {file_path}")
    data.extend(dict_data)
    try: 
        with open(file_path, "w", encoding='utf-8') as file:
            json.dump(data, file)
    except Exception as e:
        print(e)

def file_name(cur_id, n_tweets_file):
    # file name, e.g. HSpam_dataset_020.json
    number_str = str(cur_id//n_tweets_file)
    zero_filled_number = number_str.zfill(3)  # fill string with zeros, e.g 001, 023
    prefix = "HSpam_dataset_"
    file_type = ".json"
    result = prefix + zero_filled_number + file_type
    return result

def dump_tweets(l_tweets, cur_id, dir_path):
    # every 100 tweets, dump data to json
    # every 100K tweets, create a new json file
    n_tweets = 100  # number tweets per dump
    n_tweets_file = 1000 * n_tweets  # number tweets per json.file
    if l_tweets:
        if cur_id % n_tweets == 0:
            filename = file_name(cur_id, n_tweets_file)
            file_path = os.path.join(dir_path, filename)
            output_file(file_path, l_tweets)
            l_tweets = []
    return l_tweets

def run(api, tweets_db, dir_path, cur_id):
    print("Collecting Tweets...")
    l_tweets = []  # store tweets as a list
    for tweet_db in tqdm(tweets_db):
        cur_id += 1
        try:
            tweet = api.get_status(tweet_db["tweet_id"])
            tweet_feature = get_tweet_feature(tweet)
            # print(tweet_feature)
            l_tweets.append(update_tweet(cur_id, tweet_feature, tweet_db["label"]))
        except Exception as e:
            pass
        # split files
        l_tweets = dump_tweets(l_tweets, cur_id, dir_path)

def main():
    api = api_auth()
    dataset_file = "db/Pre_HSpam14_dataset.txt"
    output_dir = "db/tweet/"
    tweets_db, cur_id = parse_file(dataset_file, output_dir)
    run(api, tweets_db, output_dir, cur_id)

if __name__ == "__main__":
    main()