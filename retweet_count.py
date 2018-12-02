import tweepy #httpss://github.com/tweepy/tweepy
import csv
import glob
import csv
import collections
import os


#Twitter API credentials
consumer_key = "wX0fNPkvHM1ohbFUwdzRI04Fi"
consumer_secret = "UfHZw1ThjZ2KYpyaMq0OSmdaVaoK8ZHZvT9OBBk3uhF1vSkgqZ"
access_key = "244456805-QOi6vvviocSFl0jJKuLg99W3YGsqL8KuhdsKdxbY"
access_secret = "23N8M0sekKeiiq62GVvjtucPj3B2vCbFaCZcF7gcAnQe2"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)





    

    





def create_hashmap(screen_name , newpath1):
    names={}
    with open( os.path.join(newpath1 , '%s_followee_name.csv' % screen_name )  , 'r' , newline='' , errors="ignore" ) as csvf:
        reader = csv.DictReader(csvf)
        for row in reader:
            u = row["user"]
            names[u]=0


    return names
        

    

def get_count(screen_name, names, newpath , newpath1):
    
    
    

    
    with open( os.path.join(newpath1 ,'%s_tweets.csv' % screen_name )   , 'r' , newline='' , errors="ignore" ) as csvFile:
        reader = csv.DictReader(csvFile)
        hashmap = {}
        
        for row in reader:
                
                s = row["text"]
                ref = row["refined_tweets"]
                flag=0
                for word in s.split():
                    if(word== 'b\'RT' or word == 'b\"RT'):
                            flag=1
                            break
                            
                if(flag==1):
                    for word in s.split():
                        
                        if(word.startswith('@') and word.endswith(":")):
                           user = word[1:-1]
                           lis = []
                           
                           if user in names:
                               names[user]= names[user]+1

                               
                               if user in hashmap:
                                   lis= []
                                   lis = hashmap[user]
                                   hashmap[user] = []
                                   if ref:
                                       lis.append(ref)
                                  
                                   hashmap[user]= (lis)
                                  
                                   
                               else:
                                   lis = []
                                   if ref:
                                       lis.append(ref)
                                   
                                   hashmap[user] = lis
                           
       

        for key in hashmap:
                lists= []
                print(key)
                lists= hashmap[key] 


                with open(os.path.join(newpath ,'%s_retweets.csv' % key )  , 'w' , newline='' , errors="ignore") as f:
                            writer = csv.writer(f)
                            writer.writerow([ "retweet"])
                            for word in lists:
                              writer.writerow([word])
                            
                            
                pow

                
           

           
           
                
            
                            
                            
                
            

        retweet=[]
                   
        retweet = ( [ key , names[key] ] for key in sorted(names) )
              
        with open(    os.path.join(newpath1 ,'%s_retweet_count.csv' % screen_name ) , 'w' , newline='' , errors="ignore") as f:
                            writer = csv.writer(f)
                            writer.writerow(["user", "retweet_count"])
                            writer.writerows(retweet)
                                    
                                    
        pow
                    
                   
            
            
            
      


                

def fun(screen_name):        
        

        names={}


        print("Hi !! I am in retweet_count file")
        newpath =  '.\Data'+'_'+screen_name+'\Retweet'
        newpath1 =  '.\Data'+'_'+screen_name

        if not os.path.exists(newpath):
            os.makedirs(newpath)

           
        names=create_hashmap(screen_name , newpath1)
        get_count(screen_name, names , newpath , newpath1)




