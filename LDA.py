from __future__ import division
from nltk.corpus import wordnet as wn
import math
import sys






######################### word similarity ##########################

def get_best_synset_pair(word_1, word_2):
    """ 
    Choose the pair with highest path similarity among all pairs. 
    Mimics pattern-seeking behavior of humans.
    """
    max_sim = -1.0
    synsets_1 = wn.synsets(word_1)
    synsets_2 = wn.synsets(word_2)
    if len(synsets_1) == 0 or len(synsets_2) == 0:
        return None, None
    else:
        max_sim = -1.0
        best_pair = None, None
        for synset_1 in synsets_1:
            for synset_2 in synsets_2:
               sim = wn.path_similarity(synset_1, synset_2)
               try:
                   if sim > max_sim:
                       max_sim = sim
                       best_pair = synset_1, synset_2
               except:
                   continue
        return best_pair

def length_dist(synset_1, synset_2, ALPHA, BETA):
    """
    Return a measure of the length of the shortest path in the semantic 
    ontology (Wordnet in our case as well as the paper's) between two 
    synsets.
    """
    l_dist = sys.maxsize
    if synset_1 is None or synset_2 is None: 
        return 0.0
    if synset_1 == synset_2:
        # if synset_1 and synset_2 are the same synset return 0
        l_dist = 0.0
    else:
        wset_1 = set([str(x.name()) for x in synset_1.lemmas()])        
        wset_2 = set([str(x.name()) for x in synset_2.lemmas()])
        if len(wset_1.intersection(wset_2)) > 0:
            # if synset_1 != synset_2 but there is word overlap, return 1.0
            l_dist = 1.0
        else:
            # just compute the shortest path between the two
            l_dist = synset_1.shortest_path_distance(synset_2)
            if l_dist is None:
                l_dist = 0.0
    # normalize path length to the range [0,1]
    return math.exp(-ALPHA * l_dist)

def hierarchy_dist(synset_1, synset_2, ALPHA , BETA):
    """
    Return a measure of depth in the ontology to model the fact that 
    nodes closer to the root are broader and have less semantic similarity
    than nodes further away from the root.
    """
    h_dist = sys.maxsize
    if synset_1 is None or synset_2 is None: 
        return h_dist
    if synset_1 == synset_2:
        # return the depth of one of synset_1 or synset_2
        h_dist = max([x[1] for x in synset_1.hypernym_distances()])
    else:
        # find the max depth of least common subsumer
        hypernyms_1 = {x[0]:x[1] for x in synset_1.hypernym_distances()}
        hypernyms_2 = {x[0]:x[1] for x in synset_2.hypernym_distances()}
        lcs_candidates = set(hypernyms_1.keys()).intersection(
            set(hypernyms_2.keys()))
        if len(lcs_candidates) > 0:
            lcs_dists = []
            for lcs_candidate in lcs_candidates:
                lcs_d1 = 0
                if lcs_candidate in hypernyms_1:
                    lcs_d1 = hypernyms_1[lcs_candidate]
                lcs_d2 = 0
                if lcs_candidate in hypernyms_2:
                    lcs_d2 = hypernyms_2[lcs_candidate]
                lcs_dists.append(max([lcs_d1, lcs_d2]))
            h_dist = max(lcs_dists)
        else:
            h_dist = 0
    return ((math.exp(BETA * h_dist) - math.exp(-BETA * h_dist)) / 
        (math.exp(BETA * h_dist) + math.exp(-BETA * h_dist)))
    
def word_similarity(word_1, word_2, ALPHA, BETA):
    synset_pair = get_best_synset_pair(word_1, word_2)
    return (length_dist(synset_pair[0], synset_pair[1], ALPHA, BETA) * 
        hierarchy_dist(synset_pair[0], synset_pair[1], ALPHA, BETA))
        
########################### Main Program ###########################    


def fun(screen_name):
    
        from gensim import corpora
        import gensim
        import pandas as pd
        import os
        import csv
        ALPHA = 0.2
        BETA = 0.45

        k = 2
        w = 5
        def LDAcalculate(texts):
            # turn our tokenized documents into a id <-> term dictionary
            dictionary = corpora.Dictionary(texts)
            
            # convert tokenized documents into a document-term matrix
            corpus = [dictionary.doc2bow(text) for text in texts]

            # generate LDA model
            ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=k, id2word = dictionary, passes=20)  
            return ldamodel.print_topics(num_topics=k, num_words=w)

        def Extract(list_topics):
            topics=[]
            for topici in list_topics:
                words_list=[]
                plus_list = topici[1].split("+")
                for words in plus_list:
                    multiply_list = words.split("*")
                    i=0
                    for top in multiply_list:
                        i+=1
                        if(i==2):
                            top = top.replace('"', '')
                            words_list.append(top)
                topics.append(words_list)        
               
            return topics

        # Defining user file and it's followee's files


        path = './Data_'+screen_name
        User_File = path + '/'+screen_name+'_tweets.csv'
        Followee_Folder = path + '/Retweet'

        # importing the dataset of the user
        User_Topic = []
        texts = []
        user_data = pd.read_csv(User_File, encoding="ISO-8859-1")
        for i,row in user_data.iterrows():
            Ti = row['original_tweets']
            if type(Ti)==str and Ti and Ti.strip():
                try:
                    texts.append(Ti.split()) 
                except:
                    continue
              
        if texts:
            User_Topic = LDAcalculate(texts)

        Main_List=[]
        for topici in User_Topic:
            map_topici={}
            plus_list = topici[1].split("+")
            for words in plus_list:
                multiply_list = words.split("*")
                i=0
                val=0
                for top in multiply_list:
                    i+=1
                    if(i==1):
                        val=top
                    if(i==2):
                        top = top.replace('"', '')
                        map_topici[top]=val
            Main_List.append(map_topici)
        print(Main_List)


        Name_Topics = {}

        for filename in os.listdir(Followee_Folder):
            followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
            # list for tokenized documents in loop
            texts = []
            for i, row in followee_data.iterrows():
                Ri = row['retweet']
                if type(Ri)==str and Ri and Ri.strip():
                    try:
                        texts.append(Ri.split())
                    except:
                        continue
                    
            if filename.endswith('_retweets.csv'):
                filename = filename[:-13]
                if texts:
                    Name_Topics[filename]=Extract(LDAcalculate(texts))


        Retweet_List ={}

        for key, value in Name_Topics.items():
                Final_Ans = 0.0
                for Main_topic in Main_List:
                    Take_Sum = 0.0
                    for ki, vi in Main_topic.items():
                        both_Values = 0.0
                        for ti in value: 
                            avgi = 0.0
                            for wi in ti:
                                avgi += word_similarity(ki.replace(" ", ""), wi.replace(" ", ""), ALPHA, BETA)
                            avgi/=w
                            both_Values += avgi
                        both_Values /= k    
                        both_Values*=float(vi)
                        Take_Sum += both_Values
                    Final_Ans += Take_Sum
                Final_Ans /= k
                Retweet_List[key]=Final_Ans
             

        Followee_Folder = path + '/Mention'                 
        Name_Topics = {}

        for filename in os.listdir(Followee_Folder):
            followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
            # list for tokenized documents in loop
            texts = []
            for i, row in followee_data.iterrows():
                Ri = row['mention']
                if type(Ri)==str and Ri and Ri.strip():
                    try:
                        texts.append(Ri.split())
                    except:
                        continue
                    
            if filename.endswith('_mention.csv'):
                filename = filename[:-12]
                if texts:
                    Name_Topics[filename]=Extract(LDAcalculate(texts))

        Mention_List={}

        for key, value in Name_Topics.items():
                Final_Ans = 0.0
                for Main_topic in Main_List:
                    Take_Sum = 0.0
                    for ki, vi in Main_topic.items():
                        both_Values = 0.0
                        for ti in value: 
                            avgi = 0.0
                            for wi in ti:
                                avgi += word_similarity(ki.replace(" ", ""), wi.replace(" ", ""), ALPHA, BETA)
                            avgi/=w
                            both_Values += avgi
                        both_Values /= k    
                        both_Values*=float(vi)
                        Take_Sum += both_Values
                    Final_Ans += Take_Sum
                Final_Ans /= k
                Mention_List[key]=Final_Ans
                            
        Followee_Folder = path + '/Fav'                 
        Name_Topics = {}

        for filename in os.listdir(Followee_Folder):
            followee_data = pd.read_csv(Followee_Folder + "/" + filename, encoding="ISO-8859-1")
            # list for tokenized documents in loop
            texts = []
            for i, row in followee_data.iterrows():
                Ri = row['fav']
                if type(Ri)==str and Ri and Ri.strip():
                    try:
                        texts.append(Ri.split())
                    except:
                        continue
                    
            if filename.endswith('_fav_tweets.csv'):
                filename = filename[:-15]
                if texts:
                    Name_Topics[filename]=Extract(LDAcalculate(texts))


        heading = ['followeeName', 'Retweet_TopicScore', 'Mention_TopicScore', 'Fav_TopicScore', 'TopicScore']
        result=[]
        result.append(heading)
        Fav_List={}

        for key, value in Name_Topics.items():
                Final_Ans = 0.0
                for Main_topic in Main_List:
                    Take_Sum = 0.0
                    for ki, vi in Main_topic.items():
                        both_Values = 0.0
                        for ti in value: 
                            avgi = 0.0
                            for wi in ti:
                                avgi += word_similarity(ki.replace(" ", ""), wi.replace(" ", ""), ALPHA, BETA)
                            avgi/=w
                            both_Values += avgi
                        both_Values /= k    
                        both_Values*=float(vi)
                        Take_Sum += both_Values
                    Final_Ans += Take_Sum
                Final_Ans /= k
                Fav_List[key]=Final_Ans                    

        def normalization(data):
            key_max = max(data.keys(), key=(lambda k: data[k]))
            key_min = min(data.keys(), key=(lambda k: data[k]))    

            print('Maximum Value: ',data[key_max])
            print('Minimum Value: ',data[key_min])
            try:
                data = {k: (v-data[key_min])/(data[key_max]-data[key_min]) for k, v in data.items() }
            except:
                return data
            return data
            
        Retweet_List=normalization(Retweet_List)
        Mention_List=normalization(Mention_List)
        Fav_List=normalization(Fav_List)
        print(Fav_List)

        Total_List={}
        for key, value in Retweet_List.items():
            row=[]
            row.append(key)
            row.append(value)
            Total_List[key]=value
                      
            if key in Mention_List:
                row.append(Mention_List[key])
                Total_List[key] += Mention_List[key]
            else:
                row.append(0)
                
            if key in Fav_List:
                row.append(Fav_List[key])
                Total_List[key] += Fav_List[key]
            else:
                row.append(0)    
            result.append(row)

        for key, value in Mention_List.items(): 
            if key not in Total_List:
                row=[]
                row.append(key)
                row.append(0)
                row.append(value)
                Total_List[key] = value
                    
                if key in Fav_List:
                    row.append(Fav_List[key])
                    Total_List[key] += Fav_List[key]
                else:
                    row.append(0)            
                result.append(row) 
                
        for key, value in Fav_List.items(): 
            if key not in Total_List:
                row=[]
                row.append(key)
                row.append(0)
                row.append(0)
                row.append(value)
                Total_List[key] = value
                result.append(row)    

        Total_List=normalization(Total_List)
        #score_set = [ (x-min(score_set))/(max(score_set)-min(score_set)) for x in score_set] 
               
        for i, element in enumerate(result):
            if i!=0:
                key = element[0]
                if key in Total_List:
                    element.append(Total_List[key])

        # saving data in csv file
        with open(path + '/TopicFollowee.csv', 'w', newline='', encoding='utf-8', errors="ignore") as f:
            writer = csv.writer(f)
            for row in result:
                writer.writerow(row)        
            pow
