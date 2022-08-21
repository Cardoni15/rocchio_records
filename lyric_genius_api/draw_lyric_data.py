import pandas as pd
import numpy as np
from tqdm import tqdm
import time
from requests.exceptions import Timeout
import lyricsgenius as lg
from concurrent.futures import ThreadPoolExecutor
from nltk import flatten


#Instatiate Genius API Object
genius = lg.Genius("me-MXmuCTyJWDZ1MmERAAyivlY61EvPSD7KX2lBynV60vCOlEheYc6HVfPGlQ0ru")
genius.remove_section_headers = True


#Read in Artist Data
artist_df = pd.read_csv('./artist_track_data.csv'')



#Get's Lyrics
def get_lyrics(arg):
    index,part = arg
    for track in part.values:
        retries = 0
        while retries < 3:
            try:
                song = genius.search_song(track[3], track[1])
            except Timeout as e:
                retries += 1
                continue
            if song != None:
                lyrics.append([track[3],track[1],track[5],song.lyrics])            
            else:
                lyrics.append([track[3],track[1],track[5],np.NaN])
            break
    return True






#Splits Dataset into subdivisions
num_groups = round(artist_df.shape[0]/200, 0)
subDFs = np.array_split(artist_df, num_groups)

#Lyric Data Storage
lyrics = []

#Multithreading to run lyric data
with ThreadPoolExecutor(max_workers = 10) as exec:
    res = exec.map(get_lyrics, enumerate(subDFs))


#Convert List of Lists to DF and then to CSV
final_df = pd.DataFrame(lyrics, columns = ['track_name', 'artist_name','genre','raw_lyrics'])
final_df.to_csv('/Users/daking/Documents/GitHub/napster_2/lyric_genius_api/data3/final_lyric_data_trial_2.csv')

