#/usr/bin/python3

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re

#loads csv data into a dataframe
def load_csv(csv_filename):
    dataframe = pd.read_csv(csv_filename, encoding='utf-8')
    return dataframe

def regex_London(line):
    line = re.sub(r'London.*$',"London",line)
    return line

def regex_hyphen(line):
    line=line.replace("-"," ")
    return line

def cleanse_london(dataframe):
    series = dataframe["Place of Publication"]
    #removed London and the hyphen
    series = series.apply(regex_London)
    series=series.apply(regex_hyphen)
    dataframe["Place of Publication"]=series
    series = dataframe["Date of Publication"]
    series = series.str.extract(r'(\d{4})',expand=False)
    series= pd.to_numeric(series)
    series=series.fillna(0)
    dataframe["Date_of_Publication"]=series
    print(dataframe["Date_of_Publication"])
    return dataframe

def activity_1():
    csv_filename="Books.csv"
    df= load_csv(csv_filename)
    df = cleanse_london(df)
    no_counts=df['Place of Publication'].value_counts()
    pie_chart = no_counts.plot.pie()
    plt.show()


def activity_2():
    csv_filename="iris.data"
    name_list = ['sepal_length','sepal_width','petal_length','petal_width','species']
    df=pd.read_csv(csv_filename,names= name_list)
    groupies= df.groupby('species', as_index=False).mean()
    groupies.plot.bar(x='species')
    plt.show()

def activity_3():
    csv_filename="iris.csv"
    df = pd.read_csv(csv_filename)
    df['sepal_length']=df["sepal_length"].astype(float)
    df['sepal_width'] = pd.to_numeric(df['sepal_width'])
    df['species'] = df['species'].apply(lambda x : x.replace("Iris-","").strip())
    qf1= df.query('species == "setosa"')
    qf2= df.query('species == "virginica"')
    qf3= df.query('species == "versicolor"')
    ax1=qf1.plot.scatter(x='sepal_length',y='sepal_width', label='setosa',c='red')
    ax2=qf2.plot.scatter(x='sepal_length',y='sepal_width', label='virginica',c='blue',ax=ax1)
    ax3=qf3.plot.scatter(x='sepal_length',y='sepal_width',label='versica' ,c='green',ax=ax1)
    bx1 = qf1.plot.scatter(x='petal_length',y='petal_width', label='setosa',c='red')
    bx2 = qf2.plot.scatter(x='petal_length',y='petal_width', label='virginica',c='blue',ax=bx1)
    bx3=qf3.plot.scatter(x='petal_length',y='petal_width',label='versica' ,c='green',ax=bx1)
    plt.show()


def activity_4():
    fig, axes = plt.subplots(nrows=1, ncols=2)
    csv_filename="iris.csv"
    df = pd.read_csv(csv_filename)
    df['sepal_length']=df["sepal_length"].astype(float)
    df['sepal_width'] = pd.to_numeric(df['sepal_width'])
    df['species'] = df['species'].apply(lambda x : x.replace("Iris-","").strip())
    qf1= df.query('species == "setosa"')
    qf2= df.query('species == "virginica"')
    qf3= df.query('species == "versicolor"')
    ax1=qf1.plot.scatter(x='sepal_length',y='sepal_width', label='setosa',c='red',ax=axes[0])
    ax2=qf2.plot.scatter(x='sepal_length',y='sepal_width', label='virginica',c='blue',ax=ax1)
    ax3=qf3.plot.scatter(x='sepal_length',y='sepal_width',label='versica' ,c='green',ax=ax1)
    bx1 = qf1.plot.scatter(x='petal_length',y='petal_width', label='setosa',c='red',ax=axes[1])
    bx2 = qf2.plot.scatter(x='petal_length',y='petal_width', label='virginica',c='blue',ax=bx1)
    bx3=qf3.plot.scatter(x='petal_length',y='petal_width',label='versica' ,c='green',ax=bx1)
    plt.show()




if __name__ == '__main__':
    #remove_columns(csv_filename,columns_notneeded)
    # activity_3()
    # activity_2()
    activity_4()
