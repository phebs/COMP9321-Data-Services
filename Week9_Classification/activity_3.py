'''
Stamped by Phoebe Z
Week 9 Classification
'''
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score,recall_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import numpy as np

def train_test(submat,table):
    #classifier
    submat.fit(X_train, y_train)
    y_pred = submat.predict(X_test)
    score = accuracy_score(y_test, y_pred)
    table.append(score)

#Retrieves the csv file
df = pd.read_csv("iris.csv")

#preprocessing
X = df.iloc[:, :-1].values
y = df.iloc[:, 4].values

# #Splits the data
train,test = train_test_split(df,train_size=0.7)

#Initiate the classifiers
classifier = KNeighborsClassifier()
tree = DecisionTreeClassifier()
linear = LinearDiscriminantAnalysis()
regreLog = LogisticRegression()
clf = GaussianNB()
model = SVC()


#Storage of accuracy
scoreTable = {
    "classifier" : list(),
    "tree": list(),
    "linear": list(),
    "regreLog": list(),
    "clf": list(),
    "model":list(),
}


#Splits by Knn folds
kf = KFold(n_splits=5,shuffle=True)
for train_index, test_index in kf.split(X):
    print("TRAIN:", train_index, "TEST:", test_index)
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    train_test(classifier,scoreTable["classifier"])
    train_test(tree,scoreTable["tree"])
    train_test(linear, scoreTable["linear"])
    train_test(regreLog, scoreTable["regreLog"])
    train_test(clf, scoreTable["clf"])
    train_test(model,scoreTable["model"])

#Determines the average and stores it into a new dict
final_average =dict()
for key in scoreTable:
    average = sum(scoreTable[key])/len(scoreTable[key])
    final_average[key] = average

#Sorted the final average, reverses and stores it
sortedTable = sorted(final_average,key= lambda x: final_average[x],reverse=True)
for key in sortedTable:
    print("%s :accuracy rate %.2f%%" % (key,final_average[key]*100))