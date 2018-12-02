# Calculating cosine between two vectors
from nltk.corpus import wordnet as wn


def word_similarity(a, b):
    n = wn.synsets(a)
    g = wn.synsets(b)
    sim_vect = []
    if(len(n)>0):
        for i in g:
            if (isinstance(i.wup_similarity(n[0]), float)):
                sim_vect.append(i.wup_similarity(n[0]))
        if(sim_vect == []):
            return 0
        else:
            return max(sim_vect)
    else:
        return 0


import re
from collections import Counter

WORD = re.compile(r'\w+')


def iNeedACosine(v1, v2):
    ans = 0
    v3 = set(v1)&set(v2)
    v1 = set(v1)-set(v3)
    v2 = set(v2) - set(v3)
    ans = len(v3)
    count = len(v3)

    for a in v1:
        for b in v2:
            ans+= word_similarity(a,b)
            count = count+1
    if(ans!=0):
        ans = ans/(count)
        
    return ans

# Converting text into a vector
def iNeedAVector(text):
    words = WORD.findall(text)
    return Counter(words)

# Defining user file and it's followee's files
screen_name = "KhuranaSanya"
path = './Data_'+screen_name
User_File = path + '/'+screen_name+'_tweets.csv'
Followee_Folder = path + '/Retweet'

# Importing Packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv

# importing the dataset of the user
user_data = pd.read_csv(User_File, encoding="ISO-8859-1")

# Vector for each tweet of the user
print(screen_name)
user_vector = []
count = 0
for i,row in user_data.iterrows():
    count+=1 
    if(count>100):
        break
    T1 = row['original_tweets']
    v1 = iNeedAVector(str(T1))
    print(v1)
    if(len(v1)!=0):
        user_vector.append(v1)
    

print(len(user_vector))
heading = ['followeeName','retweet_similarity','mention_similarity','fav_similarity','TextualScore']


sum_score_TextS = {}
score_set_tweet = []
for filename in os.listdir(Followee_Folder):
    print(filename, "retweet")
    print_vector = []
    followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
    followee_vector = []
    counter = 0;
    for i, row in followee_data.iterrows():
        counter += 1;
        if(counter>100):
            break;
        Ti = row['retweet']
        tweet_vector = []
        for vect in user_vector:
            tweet_vector.append(iNeedACosine(iNeedAVector(str(Ti)),vect))
        followee_vector.append(sum(tweet_vector)/len(tweet_vector))
    if(len(followee_vector)!=0):
        followee_similarity = sum(followee_vector)/len(followee_vector)
    else:
        followee_similarity = 0
    
    if filename.endswith('_retweets.csv'):
        filename = filename[:-13]
    
    sum_score_TextS[filename]=followee_similarity
    score_set_tweet.append(sum_score_TextS[filename])
    

print("********* retweet ******************")
print(sum_score_TextS)    
    
sum_score_TextV = {}
score_set_mention = []
Followee_Folder = path + '/Mention'
for filename in os.listdir(Followee_Folder):
    print(filename, "mention")
    followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
    followee_vector = []
    counter = 0;
    for i, row in followee_data.iterrows():
        counter += 1;
        if(counter>100):
            break;
        Ti = row['mention']
        tweet_vector = []
        for vect in user_vector:
            tweet_vector.append(iNeedACosine(iNeedAVector(str(Ti)),vect))
        followee_vector.append(sum(tweet_vector)/len(tweet_vector))
    if(len(followee_vector)!=0):
        followee_similarity = sum(followee_vector)/len(followee_vector)
    else:
        followee_similarity = 0
    
    
    if filename.endswith('_mention.csv'):
        filename = filename[:-12]
    
    sum_score_TextV[filename]=followee_similarity
    score_set_mention.append(sum_score_TextV[filename])
    
print("********* mention ******************")
print(sum_score_TextV)
    
sum_score_TextF = {}
score_set_fav = []
Followee_Folder = path + '/Fav'
for filename in os.listdir(Followee_Folder):
    print(filename, "fav")
    followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
    followee_vector = []
    counter = 0
    for i, row in followee_data.iterrows():
        counter += 1;
        if(counter>100):
            break;
        Ti = row['fav']
        tweet_vector = []
        for vect in user_vector:
            tweet_vector.append(iNeedACosine(iNeedAVector(str(Ti)),vect))
        followee_vector.append(sum(tweet_vector)/len(tweet_vector))
    if(len(followee_vector)!=0):
        followee_similarity = sum(followee_vector)/len(followee_vector)
    else:
        followee_similarity = 0
    
    
    if filename.endswith('_fav_tweets.csv'):
        filename = filename[:-15]
    
    sum_score_TextF[filename]=followee_similarity
    score_set_fav.append(sum_score_TextF[filename])


    
print("********* fav ******************")
print(sum_score_TextF)

result = []  
score = []      
for k in sum_score_TextS:
    vec = []
    if((k in sum_score_TextV) and (k in sum_score_TextF)):
        print("all three same")
        print(k)
        vec.append(k)
        vec.append(sum_score_TextS[k])
        vec.append(sum_score_TextV[k])
        vec.append(sum_score_TextF[k])
        vec.append((sum_score_TextS[k]+sum_score_TextV[k]+sum_score_TextF[k])/3)
        score.append((sum_score_TextS[k]+sum_score_TextV[k]+sum_score_TextF[k])/3)
        result.append(vec)
    elif((k in sum_score_TextV) and (k not in sum_score_TextF)):
        print("retweet and mention same")
        print(k)
        vec.append(k)
        vec.append(sum_score_TextS[k])
        vec.append(sum_score_TextV[k])
        vec.append("")
        vec.append((sum_score_TextS[k]+sum_score_TextV[k])/2)
        score.append((sum_score_TextS[k]+sum_score_TextV[k])/2)
        result.append(vec)
    elif((k not in sum_score_TextV) and (k in sum_score_TextF)):
        print("retweet and fav same")
        print(k)
        vec.append(k)
        vec.append(sum_score_TextS[k])
        vec.append("")
        vec.append(sum_score_TextF[k])
        vec.append((sum_score_TextS[k]+sum_score_TextF[k])/2)
        score.append((sum_score_TextS[k]+sum_score_TextF[k])/2)
        result.append(vec)
    else:
        print("only retweets")
        print(k)
        vec.append(k)
        vec.append(sum_score_TextS[k])
        vec.append("")
        vec.append("")
        vec.append(sum_score_TextS[k])
        score.append(sum_score_TextS[k])
        result.append(vec)
        
for k in sum_score_TextV:
    vec = []
    if((k not in sum_score_TextS) and (k in sum_score_TextF)):
        print("mention and fav same")
        print(k)
        vec.append(k)
        vec.append("")
        vec.append(sum_score_TextV[k])
        vec.append(sum_score_TextF[k])
        vec.append((sum_score_TextV[k]+sum_score_TextF[k])/2)
        score.append((sum_score_TextV[k]+sum_score_TextF[k])/2)
        result.append(vec)
    elif((k not in sum_score_TextS) and (k not in sum_score_TextF)):
        print("only mention")
        print(k)
        vec.append(k)
        vec.append("")
        vec.append(sum_score_TextV[k])
        vec.append("")
        vec.append(sum_score_TextV[k])
        score.append(sum_score_TextV[k])
        result.append(vec)
    
for k in sum_score_TextF:
    vec = []
    if((k not in sum_score_TextS) and (k not in sum_score_TextV)):
        print("only fav")
        print(k)
        vec.append(k)
        vec.append("")
        vec.append("")
        vec.append(sum_score_TextF[k])
        vec.append(sum_score_TextF[k])
        score.append(sum_score_TextF[k])
        result.append(vec)
        

#normalization
for vec in result:
    vec[4] = (vec[4]-min(score))/(max(score)-min(score))

for vec in result:
    print(vec)

# creating file to store similarity of each followee with its tweets
    
with open(path+'/TextualFollowee.csv', 'w', newline='', encoding='utf-8', errors="ignore") as f:
    writer = csv.writer(f)
    writer.writerow(heading) 
    for vec in result:
        writer.writerow(vec) 
    pow
    