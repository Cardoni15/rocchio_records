<h1>Rocchio Records</h1>
<img src="https://github.com/Cardoni15/napster_2/blob/main/application_data/rocchio_logo_2.png?raw=true" width="400" height="400" align="right">
<h3> Product Overview </h3>
<ul>
  <li>Gnerate Spotify playlists based on lyrical semantics and user feedback.</li> 
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
  <li> virtualenv venv3913 --python=python3.9.13 </li>
  <li> source venv3913/bin/activate </li>
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
<li>The user needs to generate spotipy API credentials HERE </li>
<li>The user needs to generate lyric genius API credentials HERE </li>
</ul>
<h3> Generating Your First Playlist </h3>

<h3> Drawing Data from Spotify </h3>

<h3> Generating an LSI Dictionary with New Track Data </h3>





