'''
Week 10 Activity 3
Uses Agglomerative Clustering

'''

from sklearn.cluster import AgglomerativeClustering
import pandas as pd
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

#Retrieves the csv file
df = pd.read_csv("diet.csv")

#the data
data = df.drop(columns="Diet")
test = shuffle(df)

#Uses Agglomerative Clustering
cluster = AgglomerativeClustering(n_clusters=3)
cluster.fit(data)
result = cluster.labels_
cluster0 = list()
cluster1 = list()
cluster2 = list()

#Adds to respective cluster
for index, element in enumerate(result):
    if element == 0:
        cluster0.append(index)
    elif element == 1:
        cluster1.append(index)
    elif element == 2:
        cluster2.append(index)

#Allocates the clusters
cluster_0 = data.iloc[cluster0,:]
cluster_1 = data.iloc[cluster1,:]
cluster_2 = data.iloc[cluster2,:]

#plotting the graph
ax = cluster_0.plot.scatter(x='pre.weight', y='weight6weeks', label="cluster_0")
ax = cluster_1.plot.scatter(x='pre.weight', y='weight6weeks', label="cluster_1",color='green', ax=ax)
ax = cluster_2.plot.scatter(x='pre.weight', y='weight6weeks',  label="cluster_2",color='red', ax=ax)

#Mapping
map = {
    1: "Diet_1",
    2: "Diet_2",
    3: "Diet_3"
}


#Relabelling again
for index, point in test.iterrows():
    ax.text(point['pre.weight'], point['weight6weeks'], map.get(point['Diet']), color='grey', fontsize=8,verticalalignment='bottom', horizontalalignment='right')

plt.show()