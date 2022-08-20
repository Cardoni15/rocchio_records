#!/usr/bin/env python3.9
import tkinter as tk
from tkinter.ttk import *
from PIL import ImageTk, Image
import webbrowser
import json

from tkinter import * 
import tkinter.messagebox
from tkinter import ttk
import tkinterweb
from IPython.display import Audio
from urllib.request import urlopen

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

import pandas as pd
import numpy as np
import os

from search_functionality.rocchio_filter import Lyric_Rocchio_Feedback

class Rocchio_Records_GUI_Object():
    def __init__(self):
        """ 
        Initialize the GUI by creating an object
        Global variables can be stored in the init
        """
        self.rff = Lyric_Rocchio_Feedback()
        self.liked_tracks = pd.DataFrame()
        self.track_df = None
        self.track_to_rate = None
        self.like_dislike_counter = 0
        self.lyric_entered = 0
        self.like_dislike_counter = 0
        self.root_path = os.getcwd().split('/rocchio_records')[0]
        self.sp = self.init_spotify()
        # Initialize class attributes that adjust as the GUI is used.
        self.root = self.init_gui()
        self.frame0 = None
        self.frame1 = None
        self.frame2 = None
        self.frame3 = None
        self.frame1b = None
        self.label = None
        self.tu_photoimage = None
        self.td_photoimage = None
        self.r_photoimage = None
        self.p_photoimage = None
        self.logo_photoimage = None
        self.logo_label = None
        self.lyricBox = None
        self.lyricSearch = None
        self.b_like = None
        self.b_dislike = None
        self.b_neutral = None
        self.b_listen = None
        self.tracker_label = None
        self.sample_song_label = None
        self.b_startover = None
        self.b_keeprating = None
        self.b_playlist = None
        self.b_export_playlist = None
        self.listBox_lyrics = None
        self.vsb_lyrics = None
        self.listBox_playlist = None
        # this function will fill out all of the gui attributes
        self.initialze_gui_layout()
        mainloop()

    def init_spotify(self, default=False):
        """
        This function initializes a spotify object.
        This allows us to listen to music on spotify.
        """
        if default:
            # IF faulty credentials are provided default to
            # these credentials to allow for basic operation
            js = {
                    "cid" : "75124b92e97f463f8f7549a7d6f06c3f",
                    "secret" : "ff7a3e47a2a24597bad0db329fdee027",
                    "username" : "1268144208"
                }
        else:
            path = self.root_path + 'application_data/spotify_creds.txt'
            try:
                with open(path) as file:
                    data = file.read()
                js = json.loads(data)
            except:
                return self.init_spotify(default=True)
        cid = js['cid']
        secret = js['secret']
        token = util.prompt_for_user_token(
            username=js['username'],
            client_id = cid,
            client_secret = secret,
            redirect_uri = 'http://localhost:8000',
            scope=['user-modify-playback-state','user-read-playback-state']
            )
        if token:
            sp = spotipy.Spotify(auth=token)
            return sp
        else:
            # this means the user failed to provide credentials.
            # use the default creds
            return self.init_spotify(default=True)

    def generate_photo(self, photoName):
        """
        Provide a path to a photo
        return a photo object for the GUI
        """
        full_path = self.root_path + photoName
        # Creating a photoimage object to use image
        photo = PhotoImage(file = full_path)
        return photo

    def init_gui(self):
        self.root = Tk()
        self.root.geometry('640x450')
        self.root.title("Rocchio Records")
        return self.root
    #Action for clicking Get Lyric button
    def reset(self):          
        self.sample_song_label.config(text="")
        #Once 10 songs have been rated, disable most buttons and allow user to view playlist
        if self.like_dislike_counter == 10:
            self.label.config(text="Track: \nArtist: ") #, font=("Arial",12))
            self.b_like["state"] = DISABLED
            self.b_dislike["state"] = DISABLED
            self.b_neutral["state"] = DISABLED
            self.b_listen["state"] = DISABLED
            self.b_playlist["state"] = NORMAL
        elif self.lyric_entered == 0:
            self.label.config(text="Track: \nArtist: ") #, font=("Arial",12))
            self.b_like["state"] = DISABLED
            self.b_dislike["state"] = DISABLED
            self.b_neutral["state"] = DISABLED
            self.b_listen["state"] = DISABLED
        else:
            #Use the like_dislike_counter as an index!
            self.track_to_rate = self.track_df.iloc[[self.like_dislike_counter]]
            self.label.config(text = 'Track: ' + self.track_to_rate.track_name.astype('str').item() + '\n' + 'Artist: ' + self.track_to_rate.artist_name.astype('str').item())

            if self.b_like["state"] == DISABLED:
                self.b_like["state"] = NORMAL
            if self.b_dislike["state"] == DISABLED:
                self.b_dislike["state"] = NORMAL
            if self.b_neutral["state"] == DISABLED:
                self.b_neutral["state"] = NORMAL
            if self.b_listen["state"] == DISABLED:
                self.b_listen["state"] = NORMAL
            if self.b_startover["state"] == DISABLED:
                self.b_startover["state"] = NORMAL
        
    # Add 1 to the rating counter and display progress to total songs needed to rate
    def like_dislike_count(self):
        self.like_dislike_counter += 1
        self.tracker_label = Label(self.frame1, text = 'Tracks Rated: ' + str("{0:0=2d}".format(self.like_dislike_counter)) + "/10")
        self.tracker_label.grid(row=2, column=0, sticky="nw", padx=5, pady = 10)

    # Action for clicking like button: add to table at bottom of frame
    def like(self):  
        self.like_dislike_count()
        self.listBox_lyrics.insert("", "end", values=(self.track_to_rate.track_name.astype('str').item(), self.track_to_rate.artist_name.astype('str').item(), "Like")) 
        self.reset()      
        
    # Action for clicking Dislike button: add to table at bottom of frame  
    def dislike(self):  
        self.like_dislike_count()
        self.listBox_lyrics.insert("", "end", values=(self.track_to_rate.track_name.astype('str').item(), self.track_to_rate.artist_name.astype('str').item(), "Dislike")) 
        self.reset()
        
    # Action for clicking Neutral button: add to table at bottom of frame  
    def neutral(self):  
        self.like_dislike_count()
        self.listBox_lyrics.insert("", "end", values=(self.track_to_rate.track_name.astype('str').item(), self.track_to_rate.artist_name.astype('str').item(), "Neutral")) 
        self.reset()
    
    # Action for listening to the 30 second sample of each track.
    def listen_to_track(self):   
        track = self.track_to_rate.track_id.astype('str').item()
        track = self.sp.track(track)
        try:
            webbrowser.open_new(track["preview_url"])
            self.sample_song_label.config(text="Song preview playing in new window")
        except:
            self.sample_song_label.config(text="Song preview unavailable")
    
    # If you double click on a song in the display that was already rated, swap like / dislike
    def enable_edit(self,event):
        curItem = self.listBox_lyrics.focus()
        curItem_values = self.listBox_lyrics.item(curItem)['values']
        if curItem_values[2] == 'Like':
            new_rating = 'Neutral'
        elif curItem_values[2] == 'Neutral':
            new_rating = 'Dislike'
        else:
            new_rating = 'Like'
        self.listBox_lyrics.item(curItem, values=(curItem_values[0], curItem_values[1],new_rating))
        for i in self.listBox_lyrics.selection():
            self.listBox_lyrics.selection_remove(i)
        
    # Once enough songs are rated, the view playlist option displays and displays at bottom of frame
    def view_playlist(self):
        self.vsb_playlist.grid(row=1, column=1, sticky='ns')
        self.listBox_playlist.grid(row=1, column=0, sticky="ew")
        self.listBox_playlist.configure(yscrollcommand=self.vsb_playlist.set)
        # get the user's final decision on each song
        for child in self.listBox_lyrics.get_children():
            if self.listBox_lyrics.item(child)["values"][2] != 'Dislike':
                # extract the track id
                self.liked_tracks = pd.concat([self.liked_tracks, self.track_df[self.track_df.track_name == self.listBox_lyrics.item(child)["values"][0]]])
        # update the track ids for liked tracks in the rocchio feedback filter to avoid duplicates
        self.rff.update_liked_tracks(list(self.liked_tracks.track_id.unique()))
        # write the track name and artist name for the entire user playlist.
        [self.listBox_playlist.insert("", "end", values=(track[0],track[1])) for track in self.liked_tracks[['track_name', 'artist_name']].drop_duplicates().values]
        
        # reset button states for next iteration
        self.b_keeprating["state"] = NORMAL
        self.b_playlist["state"] = DISABLED
        self.b_export_playlist["state"] = NORMAL
        
    # Reset button 
    def start_over(self):
        #set flag back to 0 that no lyric has been entered yet
        self.lyric_entered = 0
        # set counter back to 0 
        self.like_dislike_counter  = -1
        self.like_dislike_count()
        # Reset buttons
        self.b_playlist["state"] = DISABLED
        self.b_keeprating["state"] = DISABLED
        self.b_export_playlist["state"] = DISABLED
        # Remove lyric
        self.label.config(text="")
        # Reset table that displays playlist
        for item in self.listBox_playlist.get_children():
            self.listBox_playlist.delete(item)
        
        # Hide playlist and scrollbar
        self.listBox_playlist.grid_forget()
        self.vsb_playlist.grid_forget()
        
        # Reset table that displays liked / disliked lyrics
        for item in self.listBox_lyrics.get_children():
            self.listBox_lyrics.delete(item)
        self.listBox_lyrics.grid(row=1, column=0, sticky="ew")
        #reset lyric search functionality (set button back to normal and clear text box)
        self.lyricSearch["state"] = NORMAL
        #lyricBox.delete("1.0","end")
        self.reset()
        
    def export_to_spotify(self):
        for index, row in self.liked_tracks.iterrows():
            try:
                self.sp.add_to_queue(row.track_id)
                self.sample_song_label.config(text="Songs have been added to your queue!")
            except:
                self.sample_song_label.config(text="Unable to add to playlist. Note: Spotify Premium required")
                break
        #sp.add_to_queue("13rC4iKtfQocWIfzPOJxaT")
        self.b_export_playlist["state"] = DISABLED

    #Action for submitting lyric in search box
    def lyric_processing(self):
        #save lyric entry into string called lyricText
        lyricText=self.lyricBox.get("1.0","end-1c")
        #disable submit button
        self.lyricSearch["state"] = DISABLED
        # This will trigger a search for similar tracks. 
        self.rff.userSearch(lyricText)
        self.rff.create_user_playlist()
        self.track_df = self.rff.return_top_10_tracks()
        self.lyric_entered = 1
        self.reset()

    def keep_rating(self):
        # this means that the user wants to keep iterating.
        # our next step is to get their likes and dislikes.
            #test out print of values in table that show likes/dislikes
        ratings = pd.Series([self.listBox_lyrics.item(child)["values"][-1] for child in self.listBox_lyrics.get_children()])
        # provide the ratings to the rocchio filter
        self.rff.apply_feedback(ratings)
        # call the filter to update the tracks
        self.rff.rocchio_feedback()
        # update the track list
        self.track_df = self.rff.return_top_10_tracks()
        self.start_over()
        self.lyric_entered = 1 
        self.reset()
        self.lyricSearch["state"] = DISABLED
        self.lyricBox["state"] = DISABLED

    def initialze_gui_layout(self):
        self.frame0 = Frame(self.root)
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.frame3 = Frame(self.root)
        # Frame for get lyric, like, dislike
        self.frame0.grid(row=0, column=0, sticky="w")
        self.frame0.grid_columnconfigure((0,1,2,3), weight=1)
        # Frame for get lyric, like, dislike
        self.frame1.grid(row=1, column=0, sticky="w")
        self.frame1.grid_columnconfigure((0,1,2,3), weight=1, uniform="column")
        #Add buttons to sub-frame in Frame 1 so they all fit in first column
        self.frame1b = Frame(self.frame1)
        self.frame1b.grid(row=1, column=0, sticky="ew")
        self.frame1b.grid_columnconfigure((0,1,2,3), weight=1, uniform="column")
        # Frame to display like / dislike selections and playlist
        self.frame2.grid(row=2, column=0, sticky="ew", rowspan=2)
        self.frame3.grid(row=5, column=0, sticky="ew")
        self.label = Label(self.frame1, text = 'Track: ' + '\n' + 'Artist: ' , anchor='w', justify=LEFT)
        self.label.grid(row=0, column=0, sticky="nw", padx=3, pady = 10, columnspan=4)
        # Add images to buttons
        self.root_path = os.getcwd().split('/rocchio_records')[0]
        self.tu_photoimage = self.generate_photo('/rocchio_records/user_interface/thumbs_up.png').subsample(6, 6)
        self.td_photoimage = self.generate_photo('/rocchio_records/user_interface/thumbs_down.png').subsample(6, 6)
        self.r_photoimage = self.generate_photo('/rocchio_records/user_interface/refresh.png').subsample(25, 25)
        self.p_photoimage = self.generate_photo('/rocchio_records/user_interface/play_button.png').subsample(12, 12)
        self.logo_photoimage = self.generate_photo('/rocchio_records/user_interface/rocchio_10.png').subsample(2, 2)
        #Add logo to top frame
        self.logo_label = Label(self.frame0, image = self.logo_photoimage)
        self.logo_label.grid(row=0, column=0)
        #Add search bar
        self.lyricBox = Text(self.frame0, height=2, width=32)
        self.lyricBox.grid(row=0, column=1, pady=5)
        self.lyricSearch = Button(self.frame0, text = 'Submit', command=self.lyric_processing)
        self.lyricSearch.grid(row=0, column=2, sticky="ew", padx=3, pady=5)
        self.lyricSearch["state"] = NORMAL
        # Create buttons (like, dislike, get lyrics, start over, view playlist)
        self.b_like = Button(self.frame1b, image = self.tu_photoimage, compound = RIGHT, command=self.like)
        self.b_like.grid(row=1, column=0, padx=3, pady=5)
        self.b_dislike = Button(self.frame1b, image = self.td_photoimage, compound = RIGHT, command=self.dislike)
        self.b_dislike.grid(row=1, column=1, padx=3, pady=5)
        self.b_neutral = Button(self.frame1b, image = self.r_photoimage, compound = RIGHT, command=self.neutral)
        self.b_neutral.grid(row=1, column=2, padx=2, pady=5)
        self.b_listen = Button(self.frame1b, image = self.p_photoimage, compound = RIGHT, command=self.listen_to_track)
        self.b_listen.grid(row=1, column=3, padx=2, pady=5)
        # Track number of lyrics liked or disliked 
        self.tracker_label = Label(self.frame1, text = 'Tracks Rated: ' + str("{0:0=2d}".format(self.like_dislike_counter)) + "/10")
        self.tracker_label.grid(row=2, column=0, sticky="nw", padx=5, pady = 10)
        # When play is clicked, display message on where song will play 
        self.sample_song_label = Label(self.frame1, text = '')
        self.sample_song_label.grid(row=1, column=1, sticky="nw", padx=5, pady = 10, columnspan=3)
        # Start over button to get back to original screen
        self.b_startover = Button(self.frame3, text = 'Start Over', command=self.start_over)
        self.b_startover.grid(row=1, column=0, sticky="ew", padx=3, pady=5)
        # Keep rating button
        self.b_keeprating = Button(self.frame3, text = 'Keep Rating', command=self.keep_rating)
        self.b_keeprating.grid(row=1, column=1, sticky="ew", padx=3, pady=5)
        # View playlist once 10 lyrics rated
        self.b_playlist = Button(self.frame3, text = 'View Playlist', command=self.view_playlist)
        self.b_playlist.grid(row=1, column=2, sticky="ew", padx=3, pady=5)
        # Export playlist to Spotify
        self.b_export_playlist = Button(self.frame3, text = 'Add to Spotify Queue', command=self.export_to_spotify)
        self.b_export_playlist.grid(row=1, column=3, sticky="ew", padx=3, pady=5)
        # Set original state for like and dislike buttons to disables
        self.b_like["state"] = DISABLED
        self.b_dislike["state"] = DISABLED
        self.b_neutral["state"] = DISABLED
        self.b_listen["state"] = DISABLED
        self.b_keeprating["state"] = DISABLED
        self.b_playlist["state"] = DISABLED
        self.b_export_playlist["state"] = DISABLED
        # create table to show lyrics with rating and add a scrollbar
        cols = ('Track Name', "Artist Name", 'Rating')
        self.listBox_lyrics = ttk.Treeview(self.frame2, columns=cols, show='headings')
        self.vsb_lyrics = ttk.Scrollbar(self.frame2, orient="vertical", command=self.listBox_lyrics.yview)
        #doubleclicking changes like to dislike and vice versa
        self.listBox_lyrics.bind("<Double-1>", self.enable_edit)
        for col in cols:
            self.listBox_lyrics.heading(col, text=col)    
        self.vsb_lyrics.grid(row=1, column=1, sticky='ns')
        self.listBox_lyrics.grid(row=1, column=0, sticky="ew")
        self.listBox_lyrics.configure(yscrollcommand=self.vsb_lyrics.set)
        # create table to show playlist - do not display until enabled
        cols = ("Track Name","Artist Name")
        self.listBox_playlist = ttk.Treeview(self.frame2, selectmode='browse', columns=cols, show='headings')
        self.vsb_playlist = ttk.Scrollbar(self.frame2, orient="vertical", command=self.listBox_playlist.yview)
        for col in cols:
            self.listBox_playlist.heading(col, text=col)
        