## Generate a prototype playlist for GUI development.
## Cody J Middleton

import pandas as pd
import os

def generate_prototype_playlist():
    """
    Return a prototype playlist in the form of a pandas dataframe
    Spotify ID, Track Name, and Artist Name
    """
    # step 1 resolve path 
    temp_path = os.getcwd()
    root_path = temp_path.split('/napster_2')[0]
    repo_path = '/napster_2/lyric_genius_api/practice_data.csv'
    practice_data_path = root_path + repo_path

    # step 2 pull 30 random tracks.
    track_df = pd.read_csv(practice_data_path)
    rel_columns = ['track_id', 'track_name', 'artist_name']
    track_df = track_df[rel_columns]
    return track_df.sample(30, random_state=15)

