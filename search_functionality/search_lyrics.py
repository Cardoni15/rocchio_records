## All functions required for search will be stored here 
# 
# Cody J Middleton 

import pandas as pd

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

