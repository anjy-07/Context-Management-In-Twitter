import sys



def fun(screen_name):
                        from gensim.models import word2vec
                        import gensim

                        pathToBinVectors = 'E:/Downloads/GoogleNews-vectors-negative300.bin.gz'

                        print("Loading the data file... Please wait...")
                        model1 = gensim.models.KeyedVectors.load_word2vec_format(pathToBinVectors, binary=True)

                        print("Successfully loaded 3.6 G bin file!")

                        # How to call one word vector?
                        # model1['resume'] -> This will return NumPy vector of the word "resume".

                        import numpy as np
                        import math
                        from scipy.spatial import distance

                        from random import sample
                        import sys
                        from nltk.corpus import stopwords
                        #from desc import *

                        class PhraseVector:
                                def __init__(self, phrase):
                                        self.vector = self.PhraseToVec(phrase)
                                def ConvertVectorSetToVecAverageBased(self, vectorSet, ignore = []):
                                        if len(ignore) == 0: 
                                                return np.mean(vectorSet, axis = 0)
                                        else: 
                                                return np.dot(np.transpose(vectorSet),ignore)/sum(ignore)

                                def PhraseToVec(self, phrase):
                                        cachedStopWords = stopwords.words("english")
                                        #phrase = phrase.lower()
                                        wordsInPhrase = [word for word in phrase.split() if word not in cachedStopWords]
                                        vectorSet = []
                                        for aWord in wordsInPhrase:
                                                try:
                                                        wordVector=model1[aWord]
                                                        vectorSet.append(wordVector)
                                                except:
                                                        pass
                                        return self.ConvertVectorSetToVecAverageBased(vectorSet)

                                # <summary> Calculates Cosine similarity between two phrase vectors.</summary>
                                # <param> name = "otherPhraseVec" description = "The other vector relative to which similarity is to be calculated."</param>
                                def CosineSimilarity(self, otherPhraseVec):
                                        cosine_similarity = np.dot(self.vector, otherPhraseVec) / (np.linalg.norm(self.vector) * np.linalg.norm(otherPhraseVec))
                                        try:
                                                if math.isnan(cosine_similarity):
                                                        cosine_similarity=0
                                        except:
                                                cosine_similarity=0		
                                        return cosine_similarity
                                



                        # Calculating cosine between two vectors
                        from nltk.corpus import wordnet as wn




                        import re
                        from collections import Counter

                        WORD = re.compile(r'\w+')


                        # Converting text into a vector

                        # Defining user file and it's followee's files

                        path = './Data_'+screen_name

                        User_File = path + '/'+screen_name+'_tweets.csv'
                        Followee_Folder = path + '/Retweet'

                        # Importing Packages
                        import numpy as np
                        import matplotlib.pyplot as plt
                        import pandas as pd
                        import os
                        import csv
                        import math

                        # importing the dataset of the user
                        user_data = pd.read_csv(User_File, encoding="ISO-8859-1")

                        # Vector for each tweet of the user
                        print(screen_name)
                        user_vector = []
                        count = 0
                        for i,row in user_data.iterrows():
                            '''count+=1 
                            if(count>100):
                                break'''
                            T1 = row['original_tweets']
                            
                            if(pd.isnull(T1)==False):
                                print(T1)
                                user_vector.append(T1)
                                
                            

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
                                '''counter += 1;
                                if(counter>100):
                                    break;'''
                                Ti = row['retweet']
                                tweet_vector = []
                                if(pd.isnull(T1)==False):  
                                    print(Ti)
                                    for vect in user_vector:
                                        tweet_vector.append( PhraseVector(vect).CosineSimilarity(PhraseVector(Ti).vector))
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
                                '''counter += 1;
                                if(counter>100):
                                    break;'''
                                Ti = row['mention']
                                tweet_vector = []
                                if(pd.isnull(T1)==False):
                                    print(Ti)
                                    for vect in user_vector:
                                        tweet_vector.append( PhraseVector(vect).CosineSimilarity(PhraseVector(Ti).vector))
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
                                '''counter += 1;
                                if(counter>100):
                                    break;'''
                                Ti = row['fav']
                                tweet_vector = []
                                if(pd.isnull(T1)==False):
                                    print(Ti)
                                    for vect in user_vector:
                                        tweet_vector.append( PhraseVector(vect).CosineSimilarity(PhraseVector(Ti).vector))
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
                            
