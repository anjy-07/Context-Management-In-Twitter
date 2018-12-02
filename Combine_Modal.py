# -*- coding: utf-8 -*-
"""
Created on Wed Feb  7 11:25:11 2018

@author: shivangi
"""

#from desc import * 
#import followee
#import mentions
#import fav
#import Read_fav
#import retweet_count
#import follower
#import LDA
#import Word2Vec_SemanticSimilarity



def fun(screen_name):
    newpath =  '.\Data'+'_'+screen_name
   
    ################ calling desc file ##############
    import desc
    desc.get_all_tweets(screen_name, newpath)


    ############### calling followee fle #############
    import followee
    followee.create_hashmap(screen_name, newpath)


    ############### calling mentions file ############
    import mentions
    mentions.fun(screen_name)


    ############### calling fav file ##############
    import fav
    fav.fun(screen_name)

    ############### calling read fv file ###########
    import Read_fav
    Read_fav.fun(screen_name)

    ############### calling retweet file ###########

    import retweet_count
    retweet_count.fun(screen_name)


    ############### calling follower file ###########

   

    ############### calling LDA file ###########

    import LDA
    LDA.fun(screen_name)

    ############### calling Word2Vec file ###########
    import Word2Vec_SemanticSimilarity
    Word2Vec_SemanticSimilarity.fun(screen_name)


    

    


    
    
    

    
    '''screen_name = "shubhi_sareen"'''
    path = './Data_'+screen_name
    import pandas as pd
    import csv
    
    heading=['followeeName', 'Final_Content_Similarity', 'Final_User_Affinity', 'User-Followee_Behaviour']
    result=[]
    result.append(heading)
    
    def normalization(data):
        key_max = max(data.keys(), key=(lambda k: data[k]))
        key_min = min(data.keys(), key=(lambda k: data[k]))    
    
        print('Maximum Value: ',data[key_max])
        print('Minimum Value: ',data[key_min])
        
        data = {k: (v-data[key_min])/(data[key_max]-data[key_min]) for k, v in data.items() }
        return data
    ########################## Content Similarity ###################################  
    
    final_score_CS = {}
    Topic_Score={}
    Textual_Score={}
    
    Topic_Score_List = pd.read_csv(path+'/TopicFollowee.csv', encoding="ISO-8859-1")
    for i,row in Topic_Score_List.iterrows():
        Fn = row['followeeName']
        TopScore = row['TopicScore']
        Topic_Score[Fn]=TopScore
    
    Text_Score = pd.read_csv(path+'/TextualFollowee.csv', encoding="ISO-8859-1")
    for i,row in Text_Score.iterrows():
        Fn = row['followeeName']
        TextScore = row['TextualScore']
        Textual_Score[Fn]=TextScore
                    
                     
    Topic_Score=normalization(Topic_Score)
    Textual_Score=normalization(Textual_Score)
                     
    for key, value in Topic_Score.items():
        row=[]
        row.append(key)
        final_score_CS[key]=value
                  
        if key in Textual_Score:
            final_score_CS[key] += Textual_Score[key]
        result.append(row)
    
    for key, value in Textual_Score.items(): 
        if key not in final_score_CS:
            row=[]
            row.append(key)
            final_score_CS[key] = value
            result.append(row)    
    
    final_score_CS=normalization(final_score_CS)
       
    for i, element in enumerate(result):
        if i!=0:
            key = element[0]
            if key in final_score_CS:
                element.append(final_score_CS[key]) 
            else:
                element.append(0)      
        
    ########################## User Affinity ###################################    
    
    final_score_UA = {}
    Retweet_List={}
    Mention_List={}
    Fav_List={}
    CommonFolloweeCount_List={}
    
    Retweet_Score = pd.read_csv(path + '/%s_retweet_count.csv' % screen_name, encoding="ISO-8859-1")
    for i,row in Retweet_Score.iterrows():
        Fn = row['user']
        RetweetScore = row['retweet_count']
        Retweet_List[Fn]=RetweetScore   
    
    Mention_Score = pd.read_csv(path + '/%s_mention_count.csv' % screen_name, encoding="ISO-8859-1")
    for i,row in Mention_Score.iterrows():
        Fn = row['user']
        MentionScore = row['mention_count']
        Mention_List[Fn]= MentionScore
                    
    
    Fav_Score = pd.read_csv(path + '/%s_fav_count.csv' % screen_name, encoding="ISO-8859-1")
    for i,row in Fav_Score.iterrows():
        Fn = row['user']
        FavScore = row['fav_count']
        Fav_List[Fn]= FavScore    
                    
    Retweet_List=normalization(Retweet_List)
    Mention_List=normalization(Mention_List)
    Fav_List=normalization(Fav_List)
                     
    for key, value in Retweet_List.items():
        final_score_UA[key]=value
                  
        if key in Mention_List:
            final_score_UA[key] += Mention_List[key]
        if key in Fav_List:
            final_score_UA[key] += Fav_List[key]
            
        if key not in final_score_CS:
            row=[]
            row.append(key)
            row.append(0)
            result.append(row)
    
    for key, value in Mention_List.items(): 
        if key not in final_score_UA:
            final_score_UA[key] = value
                          
            if key in Fav_List:
                final_score_UA[key] += Fav_List[key]
            
            if key not in final_score_CS:
                row=[]
                row.append(key)
                row.append(0)
                result.append(row)
    
    for key, value in Fav_List.items(): 
        if key not in final_score_UA:
            final_score_UA[key] = value
            
            if key not in final_score_CS:
                row=[]
                row.append(key)
                row.append(0)
                result.append(row)
    
    final_score_UA=normalization(final_score_UA)   
    
    print(result)
    for i, element in enumerate(result):
        if i!=0:
            key = element[0]
            if key in final_score_UA:
                element.append(final_score_UA[key]) 
            else:
                element.append(0)
            
    ########################## Main Program ###################################  
    
    # saving data in csv file
                
    
        
    with open(path+'/final_output.csv', 'w', newline='', encoding='utf-8', errors="ignore") as f:
        writer = csv.writer(f)
        list1 = []
        c =0
        for row in result:
            d = dict()
            if(c!=0):
                print(row[1])
                
                if(float(row[1])<0.5 and float(row[2])<0.5 and float(row[1])!=0 and float(row[2])!=0):
                    row.append("NN")
                    d["user"] = row[0]
                    list1.append(d)
                    
                elif(row[1]>=0.5 and row[2]>=0.5):
                    row.append("BO")
                elif(row[1]<0.5 and row[2]>=0.5):
                    row.append("UA")
                elif(row[1]>=0.5 and row[2]<0.5):
                    row.append("CC")
                elif( float(row[1])==0 and float(row[2])==0):
                    row.append("OO")
            c+=1
            print(row)
            #print(list1)
            writer.writerow(row)
            
        pow

   
        
        
        
    return list1
        
#print(fun())
