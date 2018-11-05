'''
Week 10 Regression analysis
'''

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
from sklearn.metrics import mean_squared_error

#Retrieves the csv file
df = pd.read_csv("diet.csv")

#splits the dataframe
x = df.drop(columns="weight6weeks")
y = df["weight6weeks"]

# #Splits the data
x_train,x_test,y_train,y_test = train_test_split(x,y,train_size=0.7)

#Create Linear Regression
linear = LinearRegression()
linear.fit(x_train,y_train)

#Predicts using the linear model
y_pred = linear.predict(x_test)
y_test = y_test.tolist()
for  i in range(len(y_pred)):
    pred = y_test[i]
    actual = y_pred[i]
    print("Prediction is %.2f" % (pred))
    print("Actual is %.2f" % (actual))

#calculate root mean squared error
error = mean_squared_error(y_test,y_pred)
print("RMSE is %.2f" % (error))