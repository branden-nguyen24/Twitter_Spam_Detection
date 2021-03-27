from tqdm import tqdm
from os import path
from os import walk
import json

def get_cur_id():
    # continue from current id as check point
    dirpath, files = scan_files()
    cur_id = 0
    if files:
        cur_file = files[-1]
        file_path = path.join(dirpath, cur_file)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                try: 
                    data = json.load(f)
                    len_data = len(data)
                    if len_data > 1:
                        cur_id = int(data[-1]["id"])
                except Exception as e:
                    print("got %s on json.load()" % e)
    return dirpath, cur_id

def parse_file(file_in, cur_id=0):
    # current ID
    tweets = []
    try:
        with open(file_in) as f:
            lines = f.readlines()
            for l in tqdm(lines):
                tweet_id, label, _ = l.split(",")
                tweet = {
                    "id": cur_id,
                    "tweet_id": tweet_id,
                    "label": label,
                }
                tweets.append(tweet)
                cur_id += 1
    except Exception as e:
        print(e)

    dirpath, cur_id = get_cur_id()
    return tweets[cur_id:], dirpath, cur_id


def scan_files():
    dir_path = "db/tweet"
    target_files = []
    for dirpath, _, filenames in walk(dir_path):            
        l_filenames = [f for f in filenames if f.endswith(".json")]
        for filename in l_filenames:
            # target_files.append(path.join(dirpath, filename))
            target_files.append(filename)
    return dirpath, sorted(target_files)
    