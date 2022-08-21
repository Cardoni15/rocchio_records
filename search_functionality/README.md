<h3> Search Functionality </h3>
This folder contains 3 files:
<ul>
  <li> Generate_LSI.ipynb </li>
  <ul> 
    <li> Fit your own latent semantic indexing objects. </li>
    <li> Learn how the LSI, TFIDF, and Concept vectors were created for the production model </li>
    <li> A basic example querys a small sample of our data for user exploration </li>
   </ul>
  <li> proto_playlist.py </li>
  <ul>
    <li> sample script demonstrating what a playlist dataframe looks like. </li>
  </ul>
  <li> rocchio_filter.py </li>
  <ul>
    <li> This is the key function driving the search and recommender system. </li>
    <li> The filter contians a class object to store all required data for a rocchio feedback filter. </li>
    <li> The LSI, TFIDF, and concept vectors are read from memory to reduce runtime. </li>
    <li> The filter uses the following parameter values:
      <ul>
        <li> Original query vector: 1.0 </li>
        <li> Liked songs vector: 0.75 </li>
        <li> Neutral song vector: 0.5 </li>
        <li> Disliked song vector: -0.25 </li>
      </ul>
     <li> The filter remembers liked and neutral songs and always provides 10 new never before seen tracks to the user </li>
   </ul>
   <li> model_performance.ipynb </li>
     <ul>
      <li> Evaluate similarity between partial lyrical matchs </li>
      <li> Generate playlists from each topic </li>
     </ul> 
     </ul>

  
  
