from os import path
from os import walk
import json
import csv

def scan_files(dir_path):
    target_files = []
    for dirpath, _, filenames in walk(dir_path):            
        l_filenames = [f for f in filenames if f.endswith(".json")]
        for filename in l_filenames:
            target_files.append(path.join(dirpath, filename))
            # target_files.append(filename)
    return sorted(target_files)

def json_dict(input_file):
    # input json file, the data is a list of dictionary
    data = []
    try:
        with open(input_file, 'r') as f:
            data = list(json.load(f))
    except Exception as e:
        print(e)
    return data

def dict_csv(data, output_file):
    cols = data[0].keys()
    with open(output_file, 'w', newline='')  as f:
        dict_writer = csv.DictWriter(f, cols)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def combine(input_dir, output_file):
    files = scan_files(input_dir)
    data = []
    print(files)
    for file in files:
        data_json = json_dict(file)
        data.extend(data_json)
    if data:
        print(f"Number of tweets: {len(data)}")
        dict_csv(data, output_file)

def main():
    input_dir = "./db/tweet/"
    output_file = "./db/tweet_dataset.csv"
    combine(input_dir, output_file)

if __name__ == "__main__":
    main()