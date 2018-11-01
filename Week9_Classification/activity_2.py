'''
Stamped by Phoebe Z
Week 9 Classification
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score,recall_score
import numpy as np

#Retrieves the csv file
df = pd.read_csv("iris.csv")

#preprocessing
X = df.iloc[:, :-1].values
y = df.iloc[:, 4].values

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

x_test = test.iloc[:,:-1].values
y_test = test.iloc[:,-1].values

y_pred = classifier.predict(x_test)
score = accuracy_score(y_test,y_pred)
#2 percentage signs = escaping from it
print("The accuracy is %.2f%%" % (score*100))

#Apply the confusion matrix
#Ci,j = i is the REAL one, and j is the PREDICTED one
# 'i' is the y-axis and 'j' is the x-axis
result = confusion_matrix(y_test, y_pred, labels=["versicolor", "virginica", "setosa"])
print(result)

#Finds the precision score
average_score = precision_score(y_test,y_pred,average="macro")
print("Precision score is %.2f" % (average_score))

#Finds the recall
recall = recall_score(y_test,y_pred,average="macro")
print("Recall score is %.2f" % (recall) )
