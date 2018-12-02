import tweepy #https://github.com/tweepy/tweepy
import csv
import glob
import csv
import collections
import re
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



hashmap ={}

def create_hashmap(screen_name , newpath1):
    names={}
    with open(   os.path.join(newpath1 , '%s_followee_name.csv' % screen_name )  , 'r' , newline='' , errors="ignore" ) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            u = row["user"]
            names[u]=0
        


    return names
        


def atfun(tweet, names , hashmap , ref, newpath1, screen_name):
     tweet = tweet.decode("utf-8")
     

    
     for word in tweet.split():
                if word.startswith('@'):
                        word = word[1:]
                        if(len(word) > 1 ): 
                                i = len(word)-1
                                if word[i] == ':' :
                                   word = word[:-1]
                                   
                        if word in names:
                            names[word]= names[word]+1
                            
                            if (word in hashmap ):
                               lis= []
                               lis = hashmap[word]
                               hashmap[word] = []
                               if ref:
                                lis.append(ref)
                               
                               hashmap[word]= (lis)
                              
                               
                            else:
                               lis = []
                               if ref:
                                   lis.append(ref)
                               
                               hashmap[word] = lis
                               

                
                 
                        
                        
   
     retweet=[]
     retweet = ( [ key , names[key] ] for key in sorted(names) )
  
     with open(     os.path.join(newpath1 ,'%s_mention_count.csv' % screen_name ), 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow(["user", "mention_count"])
                        writer.writerows(retweet) 





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











def get_alltweet(screen_name, names , newpath , newpath1 ):
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
                
                for tweet in alltweets:
                                        
                
                    atfun(tweet.text.encode("utf-8") , names , hashmap ,  refine(tweet.text.encode("utf-8")), newpath1 , screen_name)

                for key in hashmap:
                    lists= []
                    lists= hashmap[key] 

                    with open(os.path.join(newpath , '%s_mention.csv' % key ) , 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow([ "mention"])
                        
                        for word in lists:
                          writer.writerow([word])
                        
                        
                        pow
                    
                                       
              
                        
                       
                    
                                     

                

                

                
                    
                    
               
                        
                      
           
    
    
    
      


                
        
        
def fun(screen_name):
    names={}
    print("Hi !! I am in retweet_mention file")

    newpath =  '.\Data'+'_'+screen_name+'\Mention'
    newpath1 =  '.\Data'+'_'+screen_name

    if not os.path.exists(newpath):
        os.makedirs(newpath)

    
    names=create_hashmap(screen_name , newpath1)
    get_alltweet(screen_name, names , newpath , newpath1)
        

