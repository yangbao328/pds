#%%

# Text data was obtained in XML format from "SMS BACKUP AND RESTORE" App on Google play store
# Excluding all non-text data.

# imports

import pandas as pd
import datetime
import re

# ok what do we have left?
# Convert timestamp into two columns, date and time (pref in 24h)
# change type to be all "text" for when i put it into the final guy

# god is dead and i killed him.
def unixms_to_date(ms :int):
    """ Returns a YYYY-MM-DD String representation of the date represented by the ms unix timestamp. """
    ms = int(ms)
    return str(datetime.datetime.fromtimestamp(ms/1000)).split()[0]

def unixms_to_time(ms :int):
    """ Returns a HH:MM String representation of the time represented by the ms unix timestamp. """
    return str(datetime.datetime.fromtimestamp(ms/1000)).split()[1][:5]

def remove_urls(string :str):
    """ Given a string, replaces any urls in the string with empty space."""
    """ Regex from https://www.geeksforgeeks.org/python-check-url-string/"""
    string = str(string) # this is bad design but things are going into the dataframe as objects
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return re.sub(regex, "", string)

# So I can import into other files
def give_me_my_texts():
    COLUMNS_TO_DROP = ['protocol', 'address', 'toa', 'sc_toa', 'service_center', 'read', 'status', 'locked',
                    'sub_id', 'readable_date', 'contact_name', 'rr', 'sub', 'ct_t', 'read_status', 'seen',
                    'msg_box', 'sub_cs', 'resp_st', 'retr_st', 'd_tm', 'text_only', 'exp', 'm_id', 'st',
                    'creator', 'm_size', 'rpt_a', 'ct_cls', 'pri', 'tr_id', 'resp_txt', 'retr_txt_cs',
                    'ct_l', 'm_cls', 'd_rpt', 'v', '_id', 'm_type', 'parts', 'addrs', 'retr_txt', 'subject', 'date_sent']
    texts = pd.read_xml("data/jojo-texts.xml", encoding='utf-8')
    texts = texts.drop(columns=COLUMNS_TO_DROP)

    # Remove urls from texts, then drop those columns
    texts['body'] = texts['body'].apply(remove_urls)
    texts = texts[texts['body'].str.strip().astype(bool)]
    # Type is 1 if message is received, 2 if sent
    # Only want to deal with texts that I've sent
    texts = texts[texts.type == 2]

    texts['timestamp'] = texts['date']
    texts['time'] = texts['date'].apply(unixms_to_time)
    texts['date'] = texts['date'].apply(unixms_to_date)
    texts['type'] = "text"
    # Reordering
    texts = texts[["timestamp", "date", "time", "type", "body"]]
    return texts

if __name__ == "__main__":
    print(len(give_me_my_texts()))
    for line in give_me_my_texts()['body']:
        print(line)