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





    
    





def create_hashmap(screen_name,newpath):
    ids = []
    names={}
    for page in tweepy.Cursor(api.friends_ids, screen_name=screen_name).pages():
        ids.extend(page)
    for x in ids:
        
        u = api.get_user(x).screen_name
        print(u)
        u = u.strip()
        
        
        names[u]=0
       
    print(len(names))
    

    foll=[]
       
    foll = ( [ key , names[key] ] for key in sorted(names) )
  
    with open(os.path.join(newpath ,'%s_followee_name.csv' % screen_name  )   , 'w' , newline='' , errors="ignore") as f:
                        writer = csv.writer(f)
                        writer.writerow(["user", "num"])
                        writer.writerows(foll)
                        
                        
                        pow
        
           
    
    
    
      




    


    
    
      


                
        
       






        
