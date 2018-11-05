from sklearn.cluster import KMeans
import pandas as pd
from sklearn.utils import shuffle
import matplotlib.pyplot as plt
'''
Week 10 Activity 2
Uses K Means (clustering)

'''
#Retrieves the csv file
df = pd.read_csv("iris.csv")

#the data
data = df.drop(columns="species")
test = shuffle(df)

#Uses K means
kmeans = KMeans(n_clusters=3)
kmeans.fit(data)
result = kmeans.labels_
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
ax = cluster_0.plot.scatter(x='petal_length', y='petal_width', label="cluster_0")
ax = cluster_1.plot.scatter(x='petal_length', y='petal_width', label="cluster_1",color='green', ax=ax)
ax = cluster_2.plot.scatter(x='petal_length', y='petal_width',  label="cluster_2",color='red', ax=ax)

#Relabelling again
for index, point in test.iterrows():
    ax.text(point['petal_length'], point['petal_width'], point['species'], color='grey',verticalalignment='bottom', horizontalalignment='right')

plt.show()