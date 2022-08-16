#!/usr/bin/env python3.9
import tkinter as tk
from tkinter.ttk import *
from PIL import ImageTk, Image
import webbrowser

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

from search_functionality.rocchio_filter import Napster2_Rocchio_Feedback

class Napster_GUI_Object():
    def __init__(self):
        """ 
        Initialize the GUI by creating an object
        Global variables can be stored in the init
        """
        self.rff = Napster2_Rocchio_Feedback()
        self.track_df = None
        self.track_to_rate = None
        self.like_dislike_counter = 0
        self.lyric_entered = 0
        self.like_dislike_counter = 0
        self.root = Tk()
        self.root.geometry('625x450')
        self.root.title("Napster 2")
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
        temp_path = os.getcwd()
        root_path = temp_path.split('/napster_2')[0]
        tu_repo_path = '/napster_2/user_interface/thumbs_up.png'
        td_repo_path = '/napster_2/user_interface/thumbs_down.png'
        r_repo_path = '/napster_2/user_interface/refresh.png'
        p_repo_path = '/napster_2/user_interface/play_button.png'
        logo_repo_path = '/napster_2/user_interface/napster_logo.png'
        tu_path = root_path + tu_repo_path
        td_path = root_path + td_repo_path
        r_path = root_path + r_repo_path
        p_path = root_path + p_repo_path
        logo_path = root_path + logo_repo_path
        # Creating a photoimage object to use image
        tu_photo = PhotoImage(file = tu_path)
        td_photo = PhotoImage(file = td_path)
        r_photo = PhotoImage(file = r_path)
        p_photo = PhotoImage(file = p_path)
        logo_photo = PhotoImage(file = logo_path)
        # Resizing image to fit on button
        self.tu_photoimage = tu_photo.subsample(6, 6)
        self.td_photoimage = td_photo.subsample(6, 6)
        self.r_photoimage = r_photo.subsample(25, 25)
        self.p_photoimage = p_photo.subsample(12, 12)
        self.logo_photoimage = logo_photo.subsample(2, 2)
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
        self.sp = self.init_spotify()
        mainloop()

    def init_spotify(self):
        cid = '3c72f1d18da74f63addd8423fd7d668f'
        secret = '447a83ea7f494680a9bf88a43db64548'
        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

        token = util.prompt_for_user_token(
            username='12156878652',
            client_id = cid,
            client_secret = secret,
            redirect_uri = 'http://localhost:8000',
            scope=['user-modify-playback-state','user-read-playback-state']
            )
        if token:
            sp = spotipy.Spotify(auth=token)
            return sp
        return None

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
        
        #Insert songs from playlist dataframe
        for index, row in self.track_df.iterrows():
            self.listBox_playlist.insert("", "end", values=(row.track_name, row.artist_name))
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
        for index, row in self.track_df.iterrows():
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
        