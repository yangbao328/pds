import json
import pandas as pd
import glob
import datetime


# Cleaning time!
def unixus_to_date(ms :int):
    """ Returns a YYYY-MM-DD String representation of the date represented by the ms unix timestamp. """
    ms = int(ms)
    return str(datetime.datetime.fromtimestamp(ms/1000000)).split()[0]

def unixus_to_time(ms :int):
    """ Returns a HH:MM String representation of the time represented by the ms unix timestamp. """
    return str(datetime.datetime.fromtimestamp(ms/1000000)).split()[1][:5]

# Getting data in
def give_me_my_notes():
    json_files = glob.glob("./data/Keep/*.json")

    notes = []

    for path in json_files:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            notes.append(data)

    notes_df = pd.DataFrame(notes)

    notes_df
    COLUMNS_TO_DROP = ["color", "isTrashed", "isPinned", "isArchived", "title", "labels", "annotations", "attachments", "listContent"]
    notes_df = notes_df.drop(columns=COLUMNS_TO_DROP)

    notes_df["type"] = "note"

    notes_df["date"] = notes_df["userEditedTimestampUsec"].apply(unixus_to_date)
    notes_df["time"] = notes_df["userEditedTimestampUsec"].apply(unixus_to_time)

    notes_df["timestamp"] = notes_df["userEditedTimestampUsec"]
    notes_df["body"] = notes_df["textContent"]
    notes_df = notes_df[["timestamp", "date", "time", "type", "body"]]

    return notes_df