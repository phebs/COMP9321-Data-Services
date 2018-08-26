#/usr/bin/python3

import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import re

#loads csv data into a dataframe
def load_csv(csv_filename):
    dataframe = pd.read_csv(csv_filename, encoding='utf-8')
    return dataframe

 # This iterates through each cell : iterates through on rows and columns
def print_dataframe(dataframe, print_column=True, print_rows=True):
    # print column names
    line=''
    if print_column:
        print(",".join([column for column in dataframe]))

    # print rows one by one
    if print_rows:
        for index, row in dataframe.iterrows():
            line = index.strip()+","
            line+= ",".join([str(row[column]) for column in dataframe])
            print(line)


def print_full(x):
    pd.set_option('display.max_rows', len(x))
    print(x)
    pd.reset_option('display.max_rows')


def print_table(df):
    print_dataframe(df,print_rows=False)
    print(tabulate(df))


def cleansing(df):
    for column in df:
        df[column]= df[column].apply(str).apply(lambda x: x.replace(',',''))
        df[column] = pd.to_numeric(df[column])

    return df

def fix_index(line):
        line = re.sub(r'\(.*\)',"",line)
        line = re.sub(r'\[.*\]',"",line).strip()
        return line



def question_1():
    df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
    df2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    # df1.rename(columns={list(df1)[0]:'col'}, inplace=True)
    dmerged=pd.merge(df1,df2,how='inner',left_index=True,right_index=True)
    dmerged.rename(index=fix_index,inplace=True)
    print_table(dmerged)
    print_dataframe(dmerged.head(5))
    return dmerged


def question_2(dmerged):
    print("***************")
    print("Question 2")
    print("***************")
    #index has been placed to couutry already in the first question
    print(dmerged.index[0])
    return dmerged

def question_3(dmerged):
    print("***************")
    print("Question 3")
    print("***************")
    dmerged.drop('Rubish',axis=1,inplace=True)
    print_dataframe(dmerged.head(5))
    return dmerged

def question_4(dmerged):
    print("***************")
    print("Question 4")
    print("***************")
    dmerged.dropna(inplace=True)
    print_dataframe(dmerged.tail(10))
    return dmerged

def question_5(dmerged):
    print("***************")
    print("Question 5")
    print("***************")
    #Loading Summer Olympic games
    # df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
    dGold= dmerged['Gold_x'].apply(lambda x: x.replace(',',''))
    dGold = dGold.astype(float)
    # dGold=dmerged['Gold_x']
    dGold = dGold[:(len(dGold) - 1)]
    max_df=dGold.idxmax()
    print(max_df)


def question_6(dmerged):
    print("***************")
    print("Question 6")
    print("***************")
    dGoldS = dmerged['Gold_x'].apply(lambda x: x.replace(',',''))
    dGoldW= dmerged['Gold_y'].apply(lambda x: x.replace(',',''))
    dGoldS = dGoldS[:(len(dGoldS) - 1 )]
    dGoldW = dGoldW[:(len(dGoldW)) - 1 ]
    max_df = (dGoldS.astype(float) - dGoldW.astype(float)).abs().idxmax()
    print(max_df)
'''
TO DO:
Fix the filter
Fix the columns
cleans Prooperly
Show the top 5 countries and not the total
'''
def question_7(dmerged):
    print("***************")
    print("Question 7")
    print("***************")
    print(dmerged.columns)
    #Fix the columns and data 
    dmerged['Total.1']=  dmerged['Total.1'].apply(lambda x: x.replace(',',''))
    dmerged['Total.1']= dmerged['Total.1'].astype(float)
    dsorted = dmerged.sort_values(by='Total.1',axis=0,ascending=False,)
    print_table(dsorted)
    dsorted= dsorted.drop(index='Totals')
    print(dsorted.index)
    print("--------- Top 10 Rows ---------")
    print_dataframe(dsorted.head(10))
    print("--------- Bottom 10 Rows ---------")
    print_dataframe(dsorted.tail(10))
    return dsorted

def question_8(dsorted):
    print("***************")
    print("Question 8")
    print("***************")
    dsorted = cleansing(dsorted)
    dftop = dsorted.head(10)
    ax= dftop.plot.barh(y=['Total_x','Total_y'],stacked=True)
    plt.show()

def question_9(dmerged):
    print("***************")
    print("Question 9")
    print("***************")
    dmerged = cleansing(dmerged)
    Arow = dmerged.loc('Australia')
    print(Arow)
    
    



if __name__ == '__main__':
    dmerged = question_1()
    dmerged = question_2(dmerged)
    dmerged = question_3(dmerged)
    dmerged = question_4(dmerged)
    question_5(dmerged)
    question_6(dmerged)
    dsorted = question_7(dmerged)
    # question_8(dsorted)
    question_9(dmerged)

