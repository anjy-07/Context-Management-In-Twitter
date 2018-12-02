import numpy as np
from matplotlib import pyplot as plt
from sklearn import preprocessing
import csv

data=[]
with open(  'Follower_bio_similarity.csv'   , 'r' , newline='' , errors="ignore" ) as csvf:
        reader = csv.DictReader(csvf)
        i=0
        for row in reader:
            i=i+1
            
            u = row["similarity_score"]
            data.append(u)

            


data = list(map(float, data))
min_max_scaler = preprocessing.MinMaxScaler()
t = min_max_scaler.fit_transform(data)




labels = ['Similar','Dissimilar']
sim = 0
dis = 0
for x in t:
    if x > 0.7:
       sim= sim+1
    else:
       dis = dis+1



print(sim)
print(dis)

sim_score = (sim/i)*100
dis_score = (dis/i)*100

print("SIMILARTY SCORE = ")
print(sim_score)


print("DISIMILARITY SCORE =")
print(dis_score)
       
sizes = [sim , dis]
colors = ['yellow','blue']

fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
        shadow=True, startangle=90)

ax1.axis('equal')
plt.tight_layout()
plt.show()


 
#values, base = np.histogram(t, bins=40)




# red dashes, blue squares and green triangles
####plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
####plt.show()

#cumulative = np.cumsum(values)
# plot the cumulative function

#plt.plot(base[:-1], cumulative, c='blue')


#plt.show()
