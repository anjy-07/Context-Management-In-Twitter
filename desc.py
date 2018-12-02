import tweepy #https://github.com/tweepy/tweepy
import csv
import glob
import csv
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
import os
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
remove_list = ['(',')','[',']',';','_','.','-',"'",'"',',']


def refine(tweet):
    
    tweet = tweet.decode("utf-8")    
    re.sub('[:@^A-Za-z0-9!#]+', '', tweet)
    
    tweet = re.sub(r"http\S+", "", tweet)
    tweet = re.sub('@.*?:', '', tweet)
    tweet = re.sub('RT', '', tweet)
    tweet = re.sub(r"@\S+", "", tweet) 
    
    tweet = re.sub(r'[?|$|.|!@#-(\:,;"%^&*`)]',r'', tweet)
    
    stop_words = set(stopwords.words('english'))

    word_tokens = word_tokenize(tweet)

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



def atfun(tweet):
     tweet = tweet.decode("utf-8")
     atword=[]
     for word in tweet.split():
                if word.startswith('@'):
                        word = word[1:]
                        if(len(word) > 1 ): 
                                i = len(word)-1
                                if word[i] == ':' :
                                   word = word[:-1]
                 
                        atword.append(word)
                        
     return atword




def original(s):
    s = s.decode("utf-8")
    
    flag = 0
    for word in s.split():
            if(word.startswith('@') and  word.endswith(":") or word== 'RT'):
                        flag = 1
                        print("hi this is retweet or includes a mention " )

                        
                        

    if(flag == 0):
        x = refine(s.encode("utf-8"))
        
        return x
    else:
        return " "
                

                    
                       
                       
                           
                           
                           


        print(hashmap)
    

def get_all_tweets(screen_name , newpath):
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []  
        new_tweets = api.user_timeline(screen_name = screen_name,count=200 , include_rts=True)
        
        alltweets.extend(new_tweets)
        if(alltweets):
                oldest = alltweets[-1].id - 1
                while len(new_tweets) > 0:
                        print ("getting tweets before %s" % (oldest))
                        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
                        alltweets.extend(new_tweets)
                        oldest = alltweets[-1].id - 1
                        print ("...%s tweets downloaded so far" % (len(alltweets)))
                outtweets= []
                outtweets = ([tweet.id_str,  tweet.text.encode("utf-8"),
                                refine(tweet.text.encode("utf-8")) , tweet.in_reply_to_screen_name , atfun(tweet.text.encode("utf-8")) , original(tweet.text.encode("utf-8"))] for tweet in alltweets )
                
                with open(    os.path.join(newpath ,'%s_tweets.csv' % screen_name ), 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow(["id", "text", "refined_tweets" , "in_reply_to_user" , "ids_intweets" , "original_tweets" ])
                        writer.writerows(outtweets)
                        
                        pow







