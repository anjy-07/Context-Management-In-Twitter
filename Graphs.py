import retweet_count



from desc import * 
import followee
import mentions
import fav
import Read_fav
import retweet_count
import follower
import LDA
import Word2Vec_SemanticSimilarity
import Combine_Modal

print(Combine_Modal.fun())


import matplotlib.pyplot as plt
import pandas as pd

path = './Data_'+screen_name
final_data = pd.read_csv(path +'/final_output.csv')

x=[]
y=[]
NN=0
BO=0
UA=0
CC=0
for i,row in final_data.iterrows():
   x.append(row["Final_Content_Similarity"])
   y.append(row["Final_User_Affinity"])
   if(row["User-Followee_Behaviour"]=="NN"):
       NN+=1
   elif(row["User-Followee_Behaviour"]=="BO"):
       BO+=1
   elif(row["User-Followee_Behaviour"]=="UA"):
       UA+=1
   elif(row["User-Followee_Behaviour"]=="CC"):
       CC+=1
       
print(NN)

# X = [590,540,740,130,810,300,320,230,470,620,770,250]
# Y = [32,36,39,52,61,72,77,75,68,57,48,48]

#scatter plot
plt.scatter(x, y, c='red', marker='.')

# plt.plot(X, Y)

#change axes ranges
# plt.xlim(0,1000)
# plt.ylim(0,100)

#add title
plt.title('User Classification ')

#add x and y labels
plt.xlabel('Final_Content_Similarity')
plt.ylabel('Final_User_Affinity')

plt.show()

'''creating a pichart'''

import matplotlib.pyplot as plt
 
# Data to plot
labels = 'None of them', 'Content Conscious','Both', 'User Conscious' 
sizes = [NN, CC, BO, UA] 
colors = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']

 
# Plot
plt.pie(sizes, labels=labels, colors=colors,
        autopct='%1.1f%%', shadow=True, startangle=140)
 
plt.axis('equal')
plt.show()
#show plot
