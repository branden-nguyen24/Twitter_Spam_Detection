# Tweet Collection

## Dataset
### Original dataset
[HSpam14 Dataset](https://www3.ntu.edu.sg/home/AXSun/datasets.html)
* Size: 14 million tweets

### dataset collected 
[tweet_dataset.csv](https://drive.google.com/drive/u/3/folders/1uSQ58FxUK02vkOo9KkIkW7Qz2WukuLec)
* Filter original dataset `HSpam14 Dataset`
* Apply for twitter development account
* Use twitter API `tweepy` to collect tweets from tweet id in `HSpam14 Dataset`. (Since there is a limit for standard account, only can collect 50K/day)
* Store data as json files
* Size: 210,835 tweets (by April 1st, 2021)

## Feature Set
| Feature | Description |
| --- | --- |
| id | The id of tweet in original dataset |
| tweet | This is the text that was tweeted |
| no_followers | The number of followers of this twitter user |
| no_followings | The number of followings/friends of this twitter user |
| no_userfavourites | The number of favorites this twitter user received |
| no_lists | The number of lists this twitter user added |
| no_tweets | The number of tweets this twitter user sent |
| no_favorites | The number of favorites this tweet |
| no_retweets | The number of retweets this tweet |
| no_hashtags | The number of hashtags included in this tweet |
| no_usermentions | The number of user mentions included in this tweet |
| no_urls | The number of URLs included in this tweet |
| label | The class of tweet: Ham(non-spam) - 0, Spam - 1 |

