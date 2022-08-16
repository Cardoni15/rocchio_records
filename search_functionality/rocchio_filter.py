#!/usr/bin/env python3.9
## All functions required for search will be stored here 
# Cody J Middleton 

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import os
import pickle

# steps for Rocchio Feedback Filter
# PROCESS 1 convert the raw lyrics into the concept space.
# 1. Create a TFIDF vectorizer
# 2. Create a document term matrix using TFIDF vec fit_transform using the raw lyrics. [I think there is an option to lemmatize here]
# 3. Complete latent semantic indexing using TruncatedSVD(num components = num comncepts, specifiy the random state)
# 4. Fit the document term matrix using TruncatedSVD.fit_transform. THESE ARE YOUR VECTORS FOR SIMILARITY SCORING

# PROCESS 2 convert the query into a vector
# 1. Convert querry into a raw string
# 2. Use the TFIDF vectorizer above to transform the querry
# 3. Use the LSI object above to convert the querry into the concept space.

# PROCESS 3 execute the search
# 1. Find the cosine similarity between the querry and all lyrics
# 2. Sort the tracks by similarity
# 3. Return the top N tracks to the user.

# PROCESS 4 Rochhio Feedback Filtering
# 1. Group user feeback by love, no answer, dislike
# 2. Calculate the mean for each group
# 3. Apply alpha, beta, gamma, and phi to:
#       Original search, loves, hates, nuetral
# 4. Update the lyric search querry vector and return new results!

class Napster2_Rocchio_Feedback():
    """ 
    Object for containing all relevant Rocchio Search functionality
    """
    def __init__(self):
        self.query = None
        self.user_playlist = None
        self.main_path = self.base_path()
        self.lyric_vec_dict = self.load_lsi_dict_pickle()
        self.lyric_vecs = np.array(list(self.lyric_vec_dict.values()))
        self.lsiObj = self.load_lsi_pickle()
        self.tfidf = self.load_tfidf_pickle()
        self.all_tracks_df = pd.read_csv(self.main_path+'track_artist_id_df')
    
    def base_path(self):
            temp_path = os.getcwd()
            root_path = temp_path.split('/napster_2')[0]
            repo_path = '/napster_2/search_functionality/'
            return root_path + repo_path

    def userSearch(self, user_query):
        """ 
        Transform the user search string into the concept space
        """
        userVec = self.tfidf.transform([user_query])
        # convert query vec into the concept space
        userLsi = self.lsiObj.transform(userVec)
        self.query = userLsi

    def load_lsi_pickle(self):
        """ 
        read in the pickle file containing the fitted
        LSI object
        """
        temp_path = self.main_path + 'lsi_obj.p'
        with open(temp_path, 'rb') as lsi_file:
            lsiObj = pickle.load(lsi_file)
            lsi_file.close()
            return lsiObj
    
    def load_tfidf_pickle(self):
        """ 
        read in the pickle file containing the fitted
        TFIDF object
        """
        temp_path = self.main_path + 'tfidf_obj.p'
        with open(temp_path, 'rb') as tfidf_file:
            tfidf = pickle.load(tfidf_file)
            tfidf_file.close()
            return tfidf

    def load_lsi_dict_pickle(self):
        """ 
        read in the pickle file containing the fitted
        TFIDF object
        """
        temp_path = self.main_path +'lsi_vec_dict.p' 
        with open(temp_path, 'rb') as lyric_file:
            lryicVecs = pickle.load(lyric_file)
            lyric_file.close()
            return lryicVecs

    def create_user_playlist(self): #lyric_df, userLsi, lyric_vecs):
        """ 
        calculate cosine similarity between lyrics and user query
        return the top 10 in a dataframe.
        """
        # calculate cosine similarity between every track and the lyric provided.
        simVals = cosine_similarity(self.lyric_vecs, self.query)
        # create a track name, track id, artist name, similarity dataframe
        # need to make this a copy so that we do not modify the already stored data
        self.all_tracks_df['similarity'] = simVals
        self.user_playlist = self.all_tracks_df.sort_values(by='similarity', ascending=False).head(10)[['track_name', 'artist_name', 'track_id']]
        self.user_playlist['feedback'] = 0

    def return_top_10_tracks(self):
        """ 
        return the top 10 tracks based on cosine similarity
        """
        return self.user_playlist

    def apply_feedback(self, feedback_series):
        """ 
        User input assign 0,1,2 to user feedback
        0 = nuetral
        1 = dislike
        2 = love
        """
        self.user_playlist['feedback'] = feedback_series

    def rocchio_feedback(self, alpha=1.0, beta=0.75, gamma=0.25, phi=0.5):#, user_playlist, track_vec_dict, userLsi):
        """ 
        Rochhio Feedback Filtering
        1. Group user feeback by love, nuetral, dislike
        2. Calculate the mean for each group
        3. Apply alpha, beta, gamma, and phi to:
            Original search, loves, hates, nuetral
        4. Update the lyric search querry vector and return new results!
        return an updated query vector to improve search results
        """
        # create a mean vector dict for all 3 states
        meanVectDict = defaultdict(list)
        # iterate through the three states nuetral[0], dislike[1], love[2]
        for i in range(3):
            temp_tracks = self.user_playlist[self.user_playlist['feedback']==i]
            if len(temp_tracks) > 0:
                # this means that tracks with this sentiment exist.
                # we can go get the track vectors from the track_vec_dict
                tempVecs = [self.lyric_vec_dict[vec] for vec in temp_tracks['track_id']]
                # next we need to calculate the mean vector for this segment
                meanVec = np.mean(tempVecs, axis=0)
                # add this mean to the mean vect dict. The key is the state.
                meanVectDict[i] = meanVec
            else:
                # if there are no tracks in this state, set its mean to 0
                meanVectDict[i] = 0
        # calcualte the new query vector by summing all of the mean vectors together
        newQueryVec = alpha * self.query + beta * meanVectDict[2] - gamma * meanVectDict[1] + phi * meanVectDict[0]
        self.query = newQueryVec
        # update the search after making a new query vector
        self.create_user_playlist()
    