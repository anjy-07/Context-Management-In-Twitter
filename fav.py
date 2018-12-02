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











                    
                       
                       
                           
                           
                           


        

def get_all_tweets(screen_name , newpath, newpath1):
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
        alltweets = []  
        new_tweets = api.favorites(screen_name = screen_name,count=200 , include_rts=True)
        
        alltweets.extend(new_tweets)
        if(alltweets):
                oldest = alltweets[-1].id - 1
                while len(new_tweets) > 0:
                        print ("getting tweets before %s" % (oldest))
                        new_tweets = api.user_timeline(screen_name = screen_name,count=100,max_id=oldest)
                        alltweets.extend(new_tweets)
                        oldest = alltweets[-1].id - 1
                        print ("...%s tweets downloaded so far" % (len(alltweets)))
                

                outtweets = ([tweet.user.screen_name, tweet.text.encode("utf-8") , refine( tweet.text.encode("utf-8"))] for tweet in alltweets )


                with open(     os.path.join(newpath1 , '%s_fav_tweets.csv' % screen_name )   , 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow(["user", "text" , "refined" , ])
                        writer.writerows(outtweets)
                        
                        pow



def fun(screen_name):
    

        print("Hi !! I am in fav file")

        newpath =  '.\Data'+'_'+screen_name+'\Fav'
        newpath1 =  '.\Data'+'_'+screen_name

        if not os.path.exists(newpath):
            os.makedirs(newpath)
                           

        get_all_tweets(screen_name , newpath , newpath1)

