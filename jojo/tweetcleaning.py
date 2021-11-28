
import json
import pandas as pd
import datetime
import re

def remove_urls(string :str):
    """ Given a string, replaces any urls in the string with empty space."""
    """ Regex from https://www.geeksforgeeks.org/python-check-url-string/"""
    string = str(string) # this is bad design but things are going into the dataframe as objects
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return re.sub(regex, "", string)

# with open("./data/tweet.js", encoding='utf-8') as f:
#     print(f)
#     data = json.load(f)
#
# tweets = pd.json_normalize(data)
# tweets.tail(5)

# Okay. I tried doing this with the archive twitter provided, but this seems no better than using a seperate third party
# tool to pull my data. I'll just do that

# Contents of tweets-txt file pulled from allmytweets.net
def give_me_my_tweets():
    tweets = []
    month_dict = {"Jan" : 1, "Feb" : 2, "Mar" : 3, "Apr" : 4, "May" : 5, "Jun" : 6,
                  "Jul" : 7, "Aug" : 8, "Sep" : 9, "Oct" : 10, "Nov" : 11, "Dec" : 12}
    with open("./data/tweets-txt", encoding='utf-8') as f:
        for line in f:
            if line[0:2] != "RT": # Filter out retweets; only want raw jojo!
                # Get rid of newline character?
                line = line[:-1]
                temp = line.split()
                if temp[0][0] == "@": # If we're replying to someone, just get the content of the reply
                    del temp[0]
                    line = " ".join(temp)
                month = int(month_dict[temp[-3]])
                day = int(temp[-2][:-1]) #haha get rid of the comma
                year = int(temp[-1])
                post_date = datetime.date(year, month, day).isoformat()
                tweet_body = " ".join(temp[:-3])
                tweets.append((tweet_body, post_date))


    tweet_df = pd.DataFrame(tweets, columns=["body", "date"])
    tweet_df["time"] = None
    tweet_df["type"] = "tweet"
    tweet_df["timestamp"] = None
    tweet_df = tweet_df[["timestamp", "date", "time", "type", "body"]]

    tweet_df['body'] = tweet_df['body'].apply(remove_urls)
    tweet_df = tweet_df[tweet_df['body'].str.strip().astype(bool)]

    return tweet_df
