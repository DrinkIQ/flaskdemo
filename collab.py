import pandas as pd
from scipy.spatial.distance import cosine

data = pd.read_csv('converted_data.csv')

def getScore(history, similarities):
   return sum(history*similarities)/sum(similarities)

data_sims = pd.DataFrame(index=data.index,columns=data.columns)
data_sims.ix[:,:1] = data.ix[:,:1]

for i in range(0,len(data_sims.index)):
    for j in range(1,len(data_sims.columns)):
        user = data_sims.index[i]
        product = data_sims.columns[j]
 
        if data.ix[i][j] == 1:
            data_sims.ix[i][j] = 0
        else:
            product_top_names = data_neighbours.ix[product][1:10]
            product_top_sims = data_ibs.ix[product].order(ascending=False)[1:10]
            user_purchases = data_germany.ix[user,product_top_names]
 
            data_sims.ix[i][j] = getScore(user_purchases,product_top_sims)

data_recommend = pd.DataFrame(index=data_sims.index, columns=['user','1','2','3','4','5','6'])
data_recommend.ix[0:,0] = data_sims.ix[:,0]

for i in range(0,len(data_sims.index)):
    data_recommend.ix[i,1:] = data_sims.ix[i,:].order(ascending=False).ix[1:7,].index.transpose()
