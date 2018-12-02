# Calculating cosine between two vectors
import re, math
from collections import Counter
WORD = re.compile(r'\w+')
def iNeedACosine(v1, v2):
     intersection = set(v1.keys()) & set(v2.keys())
     nume = sum([v1[x] * v2[x] for x in intersection])
     test1 = sum([v1[x]**2 for x in v1.keys()])
     test2 = sum([v2[x]**2 for x in v2.keys()])
     den = math.sqrt(test1) * math.sqrt(test2)
     if not den:
        return 0.0
     else:
        return float(nume) / den

# Converting text into a vector
def iNeedAVector(text):
     words = WORD.findall(text)
     return Counter(words)

# Defining user file and it's followee's files
User_File = "./Data/div_ise_tweets.csv"
Followee_Folder = './Data/Retweet'

# Importing Packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv

# importing the dataset of the user
user_data = pd.read_csv(User_File, encoding="ISO-8859-1")

# creating file to store similarity of each followee with its tweets
fe = open('./Data/ContentSimilarUser_Tweets.csv', 'w', newline='', encoding='utf-8', errors="ignore")
writer = csv.writer(fe)

# Vector for each tweet of the user
user_vector = []
for i,row in user_data.iterrows():
    T1 = row['refined_tweets']  ## might be changed to original_tweets
    v1 = iNeedAVector(str(T1))
    user_vector.append(v1)

for filename in os.listdir(Followee_Folder):
    followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
    followee_vector = []
    for i, row in followee_data.iterrows():
        Ti = row['retweet']
        tweet_vector = []
        for vect in user_vector:
            tweet_vector.append(iNeedACosine(iNeedAVector(str(Ti)),vect))
        followee_vector.append(sum(tweet_vector)/len(tweet_vector))
    followee_similarity = sum(followee_vector)/len(followee_vector)
    print_vector = []
    if filename.endswith('_retweet.csv'):
        filename = filename[:-12]
    print_vector.append(filename)
    print_vector.append(followee_similarity)
    print(print_vector)
    writer.writerow(print_vector)
