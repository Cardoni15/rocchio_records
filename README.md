
<img src="https://github.com/Cardoni15/napster_2/blob/main/application_data/rocchio_logo_4.png?raw=true" width="900" height="175" align="top">
<h3> Product Overview </h3>
<ul>
  <li>Generate Spotify playlists based on lyrical semantics and user feedback.</li> 
  <li>The user provides their favorite song lyric.</li>
  <li>This product will provide users with a <i>unique playlist experience.</i></li>
</ul>
<h3> Techinical Overview </h3>
<ul>
  <li>A <b>Rocchio feedback filter</b> is used to generate Spotify playlists using lyrical content.</li>
  <li>Latent Semantic Indexing is used to quantify track lyrics.</li>
  <li>Cosine similarity is used to identify similar tracks.</li> 
  <li>The query vector is updated based on the positive and negative feedback provided from the user.</li>
 </ul>
 
 <h3> Getting Started </h3>
 <ul>
  <li> Open a terminal from the rocchio_records directory </li>
  <li> sudo pip install virtualenv </li>
  <li> you will need to download python 3.9 for your machine https://www.python.org/downloads/release/python-3913/ </li>
  <li> virtualenv venv39 --python=python3.9 </li>
  <li> source venv39/bin/activate </li>
  <li> pip install -r requirements.txt </li>
  <li> ./rocchio_main.py </li>
 </ul>

<h3> Repository Feature Summary </h3>
<ul>
  <li> A full user interface for generating custom playlists</li>
  <li> A notebook for querrying the spotify API for tracks</li>
  <li> A notebook for querrying the lyric Genius API for tracks</li>
  <li> A python function for creating an LSI dictionary for new tracks</li>
 </ul>
<h3> Library Requirements and Credentials </h3>
<ul>
<li>All required python libraries are stored in requirements.txt</li>
<li>No credentials required for generating a playlist</li> 
<li>Exporting a playlist to Spotify requires spotify API credentials </li>
</ul>
<h3> Generating Your First Playlist </h3>
<ul>
  <li>Enter a lyric in the search bar of the interface and submit</li>
  <li>Click like, dislike, or neutral options for the ten tracks that will display, one at a time</li>
  <li>Optionally click play for a sample of the track if user is not familiar with it</li>
  <li>Once 10 tracks are rated, view the playlist</li>
  <li>Export the playlist to Spotify or continue rating tracks for a more customized playlist</li>
</ul>
<h3> Drawing Data from Spotify and Genius </h3>
<ul>
  <li> Data can be drawn from Spotify using whatever genres you wish to draw tracks from </li>
  <li> Afterwards, the information from that can be used to return lyrical content per track using Genius </li>
  <li> The steps are as follows: </li>
  <ul>
    <li> Update genres to your liking in draw_spotify_data.py, and then run the file </li>
    <li> Then run draw_lyric_data.py and the final dataset will be exported to 'final_lyric_data.csv' </li>
   </ul>
 </ul>

<h3> Generating an LSI Dictionary with New Track Data </h3>
<ul>
  <li> A custom set of lyrics can be used to retrain the system.</li>
  <li> search_functionality/Generate_LSI.ipynb can be used to fit a new:</li>
  <ul>
    <li> TFIDF Vectorizer </li>
    <li> Latent Semantic Indexing Object </li>
    <li> {Track ID: Concept Vectors} Dictionary </li>
   </ul>
   <li> We recommend using the default objects in the repo. 75k tracks are already included. </li>
   <li> This notebook was provided in the event the user wants to retrain with a different set of tracks. </li>
   <li> More information can be found in the search_functionality read me. </li>
 </ul>
 
 <h3> Providing Spotify Credentials <i>OPTIONAL</i> </h3>
 <ul>
  <li> This is required to hear 30 second samples. </li>
  <li> This product can export playlists to spotify if user credentials are created. </li>
  <li> Log in to spotify at https://developer.spotify.com </li>
  <li> Click "create an app" and call it Rocchio Reccords </li>
  <li> Add your spotify username, CID, and secret to application_data/spotify_creds.txt </li>
  <li> Click edit settings and add 'http://localhost:8000' to the redirect_uri section. </li>
  <li> You can now add your liked songs to your queue! </li>
 <ul>




