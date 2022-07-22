import numpy as np
import pandas as pd
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm

SPOTIPY_CLIENT_ID='4f89cd57785747e1b1d7ee0b95e61985'
secret = '61708a8ace7647ba888be760fbc822d1'

#Partial List of Genres
genres_to_collect = (
    "country",
    "dance",
    "emo",
    "folk")

def create_credentials_obj():
    """
    return a spotipy object
    """
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return sp

def collect_seed_tracks(sp, genre_list, num_tracks_per_genre):
    """
    provide a genre list, number of tracks per genre
    return a dataframe of artist, track, genre
    """
    artist_genre_id_df = pd.DataFrame(columns=['artist_name', 'artist_id', 'track_name', 'track_id', 'genre'])
    if num_tracks_per_genre > 100:
        num_iterations = round(num_tracks_per_genre/100)
        num_tracks_per_genre = 100
    else:
        num_iterations = 1

    track_id_list = []
    for i in tqdm(range(num_iterations)):
        for genre in genre_list:
            tempRecs = sp.recommendations(seed_genres=[genre], limit=num_tracks_per_genre, market='US')
            for track in tempRecs['tracks']:
                temp_artist = track['artists'][0]['name']
                temp_artist_id = track['artists'][0]['id']
                temp_track_name = track['name']
                temp_track_id = track['id']
                # only assign track if it is not already in the list 
                # this avoids having tracks assigned to multiple genres
                if temp_track_id not in set(track_id_list):
                    track_id_list.append(temp_track_id)
                    # add row to dataframe
                    artist_genre_id_df.loc[len(artist_genre_id_df.index)] = [temp_artist, temp_artist_id, temp_track_name, temp_track_id, genre]
    return artist_genre_id_df

def spotify_data_booster(sp, tracks_df, num_iterations, genre_list):
    """
    read in a tracks dataframe

    use the tracks to seed more tracks

    return an updated version of the original dataframe.
    """

    track_id_list = list(tracks_df['track_id'].values)
    for i in tqdm(range(num_iterations)):
        for genre in genre_list:
            temp_df = tracks_df[tracks_df['genre']==genre]
            
            seed_tracks = list(temp_df['track_id'].sample(3))
            tempRecs = sp.recommendations(seed_genres=[genre], seed_tracks=seed_tracks, limit=95, market='US')
            for track in tempRecs['tracks']:
                temp_artist = track['artists'][0]['name']
                temp_artist_id = track['artists'][0]['id']
                temp_track_name = track['name']
                temp_track_id = track['id']
                # only assign track if it is not already in the list 
                # this avoids having tracks assigned to multiple genres
                if temp_track_id not in set(track_id_list):
                    track_id_list.append(temp_track_id)
                    # add row to dataframe
                    tracks_df.loc[len(tracks_df.index)] = [temp_artist, temp_artist_id, temp_track_name, temp_track_id, genre]
    return tracks_df

sp_creds = create_credentials_obj()
artist_track_df = collect_seed_tracks(sp_creds, genres_to_collect, 1000)
artist_track_df = spotify_data_booster(sp_creds, artist_track_df, 500, genres_to_collect)
artist_track_df.to_csv('./artist_track_data.csv')

