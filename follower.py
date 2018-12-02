import tweepy #httpss://github.com/tweepy/tweepy
import csv
import glob
import csv
import collections
import os
import time
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re



lemmatizer = WordNetLemmatizer()

ps = PorterStemmer()
#Twitter API credentials
consumer_key = "wX0fNPkvHM1ohbFUwdzRI04Fi"
consumer_secret = "UfHZw1ThjZ2KYpyaMq0OSmdaVaoK8ZHZvT9OBBk3uhF1vSkgqZ"
access_key = "244456805-QOi6vvviocSFl0jJKuLg99W3YGsqL8KuhdsKdxbY"
access_secret = "23N8M0sekKeiiq62GVvjtucPj3B2vCbFaCZcF7gcAnQe2"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)





def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except  (tweepy.RateLimitError, ConnectionError, UnicodeEncodeError, tweepy.TweepError) as exc:
            time.sleep(960)    
    








remove_list = ['(',')','[',']',';','_','.','-',"'",'"',',']


def refine(tweet):
    
        
    re.sub('[:@^A-Za-z0-9!#]+', '', tweet)
    
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub('@.*?:', '', tweet)
    tweet = re.sub('RT', '', tweet)
    tweet = re.sub(r"@\S+", "", tweet) 
    
    tweet = re.sub(r'[?|$|.|!@#-(\:,;"%^&*`)]',r'', tweet)
    
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(tweet)
    filtered_sentence=[]
    for w in word_tokens:
        if not w in stop_words:
            filtered_sentence.append(w)
    filtered_sentence = [lemmatizer.lemmatize(ps.stem(w)) for w in word_tokens if not w in stop_words]    
    word_list=[]
    for w in filtered_sentence:
        for remov in remove_list:
            rem = "\\"+remov
            w = re.sub(rem, '', w)
        word_list.append(w)
            
    word_list = [w for w in word_list if re.match(r'[A-Z]+', w, re.I)] 
    write_comment = ' '.join(word for word in word_list)
    
    return write_comment






def create_hashmap(screen_name,names , newpath , description):
    ids = []
    names={}
    
    for page in tweepy.Cursor(api.followers_ids, screen_name=screen_name).pages():
        ids.extend(page)
    for x in ids:
        
        u = api.get_user(x).screen_name
        desc = api.get_user(x).description
        
        u = u.strip()
        print(u)
        
        
        names[u]=refine(desc)
       
            
        
    print(len(names))
    

    foll=[]
       
    foll = ( [ key , names[key] ] for key in sorted(names) )
  
    with open(os.path.join(newpath ,'%s_follower_name.csv' % screen_name  )   , 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow(["user", "desc"])
                        writer.writerow([screen_name , description])
                        writer.writerows(foll)
                        
                        
                        pow
        
           
    
    
    
      


    
      




    


    
    
      


def fun(screen_name):                
        
        names={}
        print("Hi !! I am in  follower file")
        newpath =  '.\Data'+'_'+screen_name
        u = api.get_user(screen_name)

        if not os.path.exists(newpath):
            os.makedirs(newpath)

        create_hashmap(screen_name, names , newpath , u.description)



                
