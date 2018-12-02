# -*- coding: utf-8 -*-
"""
Created on Tue May  1 12:16:34 2018

@author: ashima
"""

# Defining user file and it's followee's files
screen_name = "KhuranaSanya"
path = './Data_'+screen_name
User_File = path + '/'+screen_name+'_follower_name.csv'

# Importing Packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import csv
import math

#Import all the dependencies
import gensim
from nltk import RegexpTokenizer
from nltk.corpus import stopwords
from gensim.models.deprecated.doc2vec import LabeledSentence

# importing the dataset of the user
user_data = pd.read_csv(User_File, encoding="ISO-8859-1")

data = []
labelsList = []

for i,row in user_data.iterrows():
    print(row["user"])
    print("----")
    print(row["desc"])
    if(pd.isnull(row["desc"])==False):
        data.append(row["desc"])
        labelsList.append(row["user"])
    
##print(data)

tokenizer = RegexpTokenizer(r'\w+')

def nlp_clean(data):
   new_data = []
   for d in data:
      dlist = tokenizer.tokenize(d)
      new_data.append(dlist)
   return new_data


class LabeledLineSentence(object):
    def __init__(self, doc_list, labels_list):
        self.labels_list = labels_list
        self.doc_list = doc_list
    def __iter__(self):
        for idx, doc in enumerate(self.doc_list):
              yield gensim.models.deprecated.doc2vec.LabeledSentence(doc,[self.labels_list[idx]])
              

data = nlp_clean(data)

print(data)

#iterator returned over all documents
it = LabeledLineSentence(data, labelsList)

model = gensim.models.Doc2Vec(size=300, min_count=0, alpha=0.025, min_alpha=0.025)
model.build_vocab(it)

#training of model
for epoch in range(100):
    print("model saved")
    print('iteration ',str(epoch+1))
    model.train(it,total_examples=model.corpus_count, epochs = model.epochs)
    model.alpha -= 0.002
    model.min_alpha = model.alpha
#saving the created model
model.save('doc2vec.model')
print("model saved")    

#loading the model
d2v_model = gensim.models.doc2vec.Doc2Vec.load('doc2vec.model')

result = []

for i in range(1,len(labelsList)):
    print(labelsList[0],labelsList[i])
    docs_similarity = d2v_model.docvecs.similarity(0,i)
    print("***********************************")
    print(docs_similarity)
    pre_result = []
    pre_result.append(labelsList[i])
    pre_result.append(docs_similarity)
    result.append(pre_result)
    

##store similarity in file
heading = ['follower_name','similarity_score']
with open(path+'/Follower_bio_similarity.csv', 'w', newline='', encoding='utf-8', errors="ignore") as f:
    writer = csv.writer(f)
    writer.writerow(heading) 
    for vec in result:
        writer.writerow(vec) 
    pow
    
