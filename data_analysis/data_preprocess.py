import pandas as pd
import re

# data preprocessing
from string import punctuation
from nltk.corpus import stopwords


def main():
    filename = "tweet_dataset.csv"
    input_path = filename
    output_path = f"clean_{filename}"
    run(input_path, output_path)


def run(input_path, output_path):
    # 1. load file
    df = read_csv(input_path)
    # 2. data preprocess
    if not df.empty:
        # drop irrelevant columns "id"
        cols = ["id"]
        df_drop = drop_column(df, cols)
        # wording preprocessing
        df_pre = data_preprocess(df_drop)
        df_pre = move_column_last_to_first(df_pre)

        # 3. output file
        if not df_pre.empty:
            output_csv(df_pre, output_path)
    return df


def output_csv(df, output_path):
    # if file does not exist write header
    with open(output_path, "w") as f:
        df.to_csv(f, mode="a", index=False, header=not f.tell(), encoding="utf-8")

    print(f"File {output_path} outputted")
    print("Finished!!!")


def read_csv(input_path):
    # 1. load file
    try:
        df = pd.read_csv(input_path, engine="python")
        print(f"file {input_path} loaded")
        return df
    except Exception as e:
        print(e)
        return


def move_column_last_to_first(df):
    # move the last column to the first
    try: 
        cols = df.columns.tolist()
        update_cols = [cols[-1]].extend(cols[:-1])
        df = df[update_cols]
    except Exception as e:
        print(e)
        print("Failed to move columns")
    return df


def drop_column(df, cols):
    # drop irrelevant columns
    try:
        df = df.drop(columns=cols)
        print(f"columns {cols} dropped")
    except Exception as e:
        print(e)
    return df


def data_preprocess(df):
    print("Data preprocessing...")
    # Data preprocess
    df["tweet_clean"] = df["tweet"]
    # lower case
    print("lowerring case...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: str(x).lower())
    # remove unicode
    print("removing unicode...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_unicode(x))
    # remove url
    print("removing url...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_url(x))
    # removes hastag in front of a word
    print("removing hastag in front of a word...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_hashtag(x))
    # removes emoticons from tweet
    print("removing emoticons from tweet...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_emoticons(x))
    # remove punctuation
    print("removing punctuation...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_punctuation(x))
    # remove stop words
    print("removing stop words...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_stop_words(x))
    # removes integers
    print("removing integers...")
    df["tweet_clean"] = df["tweet_clean"].apply(lambda x: remove_numbers(x))

    return df


def remove_stop_words(text):
    """Remove stop words"""
    nltk_stop = stopwords.words("english")
    text = " ".join([c for c in text.split() if c not in nltk_stop])
    return text


def remove_unicode(text):
    """ Removes unicode strings like "\u002c" and "x96" """
    text = re.sub(r"(\\u[0-9A-Fa-f]+)", r"", text)
    text = re.sub(r"[^\x00-\x7f]", r"", text)
    return text


def remove_url(text):
    """ Replaces url address with "url" """
    text = re.sub("((www\.[^\s]+)|(https?://[^\s]+))", "", text)
    return text


def remove_hashtag(text):
    """ Removes hastag in front of a word """
    text = re.sub(r"#([^\s]+)", r"\1", text)
    return text


def remove_numbers(text):
    """ Removes integers """
    text = "".join([i for i in text if not i.isdigit()])
    return text


def remove_emoticons(text):
    """ Removes emoticons from text """
    text = re.sub(
        ":\)|;\)|:-\)|\(-:|:-D|=D|:P|xD|X-p|\^\^|:-*|\^\.\^|\^\-\^|\^\_\^|\,-\)|\)-:|:'\(|:\(|:-\(|:\S|T\.T|\.\_\.|:<|:-\S|:-<|\*\-\*|:O|=O|=\-O|O\.o|XO|O\_O|:-\@|=/|:/|X\-\(|>\.<|>=\(|D:",
        "",
        text,
    )
    return text


def remove_punctuation(text):
    """remove punctuation"""
    text = text.translate(str.maketrans("", "", punctuation))
    return text


if __name__ == "__main__":
    main()
