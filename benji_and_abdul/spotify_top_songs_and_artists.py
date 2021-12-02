import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Converts a jsonfile to a dataframe, in this case, omits the endTime column
def convert_json_to_df(json_file):
    json_df = pd.read_json(json_file)
    json_df = json_df.loc[:, ~json_df.columns.isin(["endTime"])]
    return json_df


# Uses the given dataframe to fill up a dictionary
def fill_dicts(df, dict_songs, dict_artists):
    for index, row in df.iterrows():
        song = row["trackName"]
        msPlayed = row["msPlayed"]
        artist = row["artistName"]
        if song in dict_songs:
            dict_songs[song] = dict_songs[song] + msPlayed
        else:
            dict_songs[song] = msPlayed
        if artist in dict_artists:
            dict_artists[artist] = dict_artists[artist] + msPlayed
        else:
            dict_artists[artist] = msPlayed


# Sorts a dictionary by value
def sort_dict(dictionary):
    sorted_dict = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)
    return sorted_dict


# Converts a tuple-based dictionary into a dictionary that can be converted into a dataframe, for example
# {Artist1 : Song1, Artist2 : Song2} --> {Artists: [Artist1, Artist2], Songs: [Song1, Song2]}
def get_updated_dict(old_dict, key_label):
    keys = list(old_dict.keys())[:20]
    msPlayed = list(old_dict.values())[:20]
    # Conversion from milliseconds to minutes
    msPlayed = [time / 60000 for time in msPlayed]
    updated_dict = {key_label: keys, "Minutes Played": msPlayed}
    return updated_dict


# Uses seaborn to visualize a bar plot with the given title
def plot_dict(sorted_dict, title, y_label):
    df = pd.DataFrame(sorted_dict)
    sns.barplot(x="Minutes Played", y=y_label, data=df, palette="plasma").set(title=title)
    plt.tight_layout()
    plt.show()


def plot_benjis_top_songs_and_artists():
    # Contains songs and corresponding milliseconds played
    songs_dict = {}

    # Contains artists and corresponding milliseconds played
    artists_dict = {}

    # Gets dataframe from three json files gotten from Spotify
    df0 = convert_json_to_df("StreamingHistory0.json")
    df1 = convert_json_to_df("StreamingHistory1.json")
    df2 = convert_json_to_df("StreamingHistory2.json")

    # Fills the dictionaries
    fill_dicts(df0, songs_dict, artists_dict)
    fill_dicts(df1, songs_dict, artists_dict)
    fill_dicts(df2, songs_dict, artists_dict)

    # Get the dictionaries sorted by value
    songs_dict = dict(sort_dict(songs_dict))
    artists_dict = dict(sort_dict(artists_dict))

    # Converts the dictionaries we created into dictionaries that can be converted to a dataframe, this
    # is further explained in the function's purpose statement
    songs_updated = get_updated_dict(songs_dict, "Songs")
    artists_updated = get_updated_dict(artists_dict, "Artists")

    # Plots top 20 songs and artists
    plot_dict(songs_updated, "Benji's Top 20 Songs", "Songs")
    plot_dict(artists_updated, "Benji's Top 20 Artists", "Artists")


def plot_abduls_top_songs_and_artists():
    # Contains songs and corresponding milliseconds played
    songs_dict = {}

    # Contains artists and corresponding milliseconds played
    artists_dict = {}

    # Gets dataframe from three json files gotten from Spotify
    df0 = convert_json_to_df("StreamingHistory3.json")

    # Fills the dictionaries
    fill_dicts(df0, songs_dict, artists_dict)

    # Get the dictionaries sorted by value
    songs_dict = dict(sort_dict(songs_dict))
    artists_dict = dict(sort_dict(artists_dict))

    # Converts the dictionaries we created into dictionaries that can be converted to a dataframe, this
    # is further explained in the function's purpose statement
    songs_updated = get_updated_dict(songs_dict, "Songs")
    artists_updated = get_updated_dict(artists_dict, "Artists")

    # Plots top 20 songs and artists
    plot_dict(songs_updated, "Abdul's Top 20 Songs", "Songs")
    plot_dict(artists_updated, "Abdul's Top 20 Artists", "Artists")


if __name__ == '__main__':
    plot_benjis_top_songs_and_artists()
    plot_abduls_top_songs_and_artists()
