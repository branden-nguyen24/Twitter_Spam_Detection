from tqdm import tqdm
from os import path
from os import walk
import json

def get_cur_id(dir_path):
    # continue from current id as check point
    files = scan_files(dir_path)
    cur_id = 0
    if files:
        cur_file = files[-1]
        file_path = path.join(dir_path, cur_file)
        if path.isfile(file_path):
            with open(file_path, "r") as f:
                try: 
                    data = json.load(f)
                    len_data = len(data)
                    if len_data > 1:
                        cur_id = int(data[-1]["id"])
                except Exception as e:
                    print("got %s on json.load()" % e)
    return cur_id

def parse_file(file_in, dir_path):
    # current ID
    tweets = []
    try:
        print("Parsing source file...")
        with open(file_in) as f:
            lines = f.readlines()
            for id, l in enumerate(tqdm(lines)):
                tweet_id, label, _ = l.split(",")
                tweet = {
                    "id": id,
                    "tweet_id": tweet_id,
                    "label": label,
                }
                tweets.append(tweet)
    except Exception as e:
        print(e)

    cur_id = get_cur_id(dir_path)
    return tweets[cur_id:], cur_id


def scan_files(dir_path):
    target_files = []
    for _, _, filenames in walk(dir_path):            
        l_filenames = [f for f in filenames if f.endswith(".json")]
        for filename in l_filenames:
            # target_files.append(path.join(dirpath, filename))
            target_files.append(filename)
    return sorted(target_files)
    