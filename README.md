Followee Management: Helping Users Follow the Right Users on Online Social Media

Paper Published in IEEE:- https://ieeexplore.ieee.org/abstract/document/8508517

Conference/Workshop:
--------------------
http://cnd.iit.cnr.it/sao2018/sub.html


Data Collection
---------------
1. desc.py: Collects ~3k tweets for a given user defined with screen_name. Tweets are stored in data folder as <screen_name>_tweets.csv file

2. followee.py: Collects names of all followees of a given user with screen_name and stores them in <screen_name>_followee_name.csv file:

3. retweet_count.py: Reads <screen_name>_tweets.csv file to get all tweets from a user. For each tweet, it checks for "RT" pattern, whenever found it increments retweeted count for that followee. Output is list of all followees along with their retweet count as <screen_name>_retweet_count.csv

4. fav.py: Collects those tweets from followees which have been favorited by given user and stores those favourited tweets in <screen_name>_fav_tweets.csv

5. Read_fav.py: Reads <screen_name>_fav_tweets.csv and computes number of times followee's tweets have been favourited by given user and stores in <screen_name>_fav_count.csv file

6. mention.py: Computes number of times each followee is mentioned in the tweets posted by the given user and saves it in <screen_name>_mention_count.py

7. follower.py: Collects names of all followers along with their bio text for a given user and stores in <screen_name>_follower_name.csv file.


Content Affinity with followees
-------------------------------

LDA (Topic)
-----------
8. LDA.py computes topics related to original tweets posted by given user and retweets, mentioned tweets & favourited tweets w.r.t. followees and finds similarity between topics of original tweets with retweets, mentioned tweets & favourited tweets of each followee and stores in TopicFollowee.csv file

Textual Similarity (Word2Vec)
-----------------------------

9. a) SemanticSimilarity.py computes semantic similarity of original tweets of a given user with retweets, mentioned tweets & favourited tweets of each followee and stores in TextualFollowee.csv file (WordNet)

   b) Word2Vec_SemanticSimilarity.py computes semantic similarity of original tweets of a given user with retweets, mentioned tweets & favourited tweets of each followee and stores in TextualFollowee.csv file (Google Word2Vec)

Total Content Similarity Score
------------------------------

10. a) Combine_Modal.py computes combined content similarity score by taking normalized scores of LDA and Textual similarities
Result stored in final_output.csv

User Affinity Score
-------------------

10. b) Combine_Model.py computes user affinity score based on retweet count, mention count and favorited count
Result stored in final_output.csv


User Categorization
-------------------

10. c) Combine_Model.py computes user categories taking thresholds as 0.5


User Behavior Towards Followees (Scatter Plot)
-----------------------------------------------

11. Graphs.py plots scatter plot between user affinity and content affinity (Fig.4 in report)


Bio-Similarity
--------------

12. doc2vec_bio_similarity.py takes as input followers' bio text from <screen_name>_follower_name.csv file, uses doc2vec model to compute similarity of given user's bio with the bio of all followers and saves output in Follower_bio_similarity.csv file.





