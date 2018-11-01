'''
Stamped by Phoebe Z
Week 9 Classification
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

#Retrieves the csv file
df = pd.read_csv("iris.csv")

# #Splits the data
train,test = train_test_split(df,train_size=0.7)

# Splits the model
model = train.drop(columns="species")
target = train["species"]

#Starts the knn classifier
classifier = KNeighborsClassifier()
classifier.fit(model.iloc[:],target.iloc[:])

# Testing the data
print("Testing the data...")


for index,flower in test.iterrows():
    features = np.reshape(flower.tolist()[:-1],(1,-1))
    actual = flower[-1]
    print("The prediction is " + classifier.predict(features))
    print("Correct answer " + str(actual))


