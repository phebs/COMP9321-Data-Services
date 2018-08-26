#/usr/bin/python3

import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
from matplotlib import *
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

def print_series(dataframe):
    line_index = ",".join([str(key) for key in dataframe.index])
    line_row = ",".join([str(values) for values in dataframe])
    print(line_index)
    print(line_row)


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
    print("*********************************************")
    print("Question 1")
    print("*********************************************")
    df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
    df2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
    column_rename = {"Number of Games the country participated in_x" : "no_Games_Country_Participated_Summer", 
                    "Gold_x":"Gold_Summer",
                    "Silver_x":"Silver_Summer",
                    "Bronze_x":"Bronze_Summer",
                    "Total_x":"Total_Summer",
                    "Number of Games the country participated in_y" : "no_Games_Country_Participated_Winter",
                    "Gold_y":"Gold_Winter",
                    "Silver_y":"Silver_Winter",
                    "Bronze_y":"Bronze_Winter",
                    "Total_y":"Total_Winter",
                    "Number of Games the country participated in.1":"no_Games_Country_Participated_Total",
                    "Gold.1":"Gold_Total",
                    "Silver.1":"Silver_Total",
                    "Bronze.1":"Bronze_Total",
                    "Total.1":"Total_Medals"
                    }
    dmerged=pd.merge(df1,df2,how='inner',left_index=True,right_index=True)
    dmerged.rename(columns=column_rename,inplace=True)
    # dmerged.rename(index=fix_index,inplace=True)
    print_table(dmerged)
    print_dataframe(dmerged.head(5))
    return dmerged


def question_2(dmerged):
    print("*********************************************")
    print("Question 2")
    print("*********************************************")
    #index has been placed to country already in the first question
    series = dmerged.iloc[0]
    print_series(series)
    return dmerged

def question_3(dmerged):
    print("*********************************************")
    print("Question 3")
    print("*********************************************")
    dmerged.drop('Rubish',axis=1,inplace=True)
    print_dataframe(dmerged.head(5))
    return dmerged

def question_4(dmerged):
    print("*********************************************")
    print("Question 4")
    print("*********************************************")
    dmerged.dropna(inplace=True)
    print_dataframe(dmerged.tail(10))
    return dmerged

def question_5(dmerged):
    print("*********************************************")
    print("Question 5")
    print("*********************************************")
    dmerged = cleansing(dmerged)
    #Loading Summer Olympic games
    # df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
    dGold=dmerged['Gold_Summer']
    dGold = dGold[:(len(dGold) - 1)]
    max_df=dGold.idxmax()
    print(str(max_df) + " contains " + str(dGold.loc[max_df]) + " Gold medals")
    return dmerged


def question_6(dmerged):
    print("*********************************************")
    print("Question 6")
    print("*********************************************")
    dGoldS = dmerged['Gold_Summer']
    dGoldW= dmerged['Gold_Winter']
    dGoldS = dGoldS[:(len(dGoldS) - 1 )]
    dGoldW = dGoldW[:(len(dGoldW)) - 1 ]
    max_df = (dGoldS - dGoldW).abs().idxmax()
    print(max_df + "has the highest difference between Summer and Winter Gold medals")
'''
TO DO:
Fix the filter
Fix the columns
cleans Prooperly
Show the top 5 countries and not the total
'''
def question_7(dmerged):
    print("*********************************************")
    print("Question 7")
    print("*********************************************")
    #Fix the columns and data 
    # dmerged['Total.1']=  dmerged['Total.1'].apply(lambda x: x.replace(',',''))
    # dmerged['Total.1']= dmerged['Total.1'].astype(float)
    dsorted = dmerged.sort_values(by='Total_Medals',axis=0,ascending=False,)
    print_table(dsorted)
    # dsorted= dsorted.drop(index='Totals')
    print("--------- Top 5 Rows ---------")
    print_dataframe(dsorted.head(5))
    print("--------- Bottom 5 Rows ---------")
    print_dataframe(dsorted.tail(5))
    return dsorted

def question_8(dsorted):
    print("*********************************************")
    print("Question 8")
    print("*********************************************")
    dsorted.rename(index=fix_index,inplace=True)
    dftop = dsorted.head(10)
    ax= dftop.plot.barh(y=['Total_Summer','Total_Winter'],stacked=True, title='Medals for Winter and Summer Games')
    ax.legend(["Summer Games","Winter Games"])
    plt.show()

def question_9(dmerged):
    print("*********************************************")
    print("Question 9")
    print("*********************************************")
    dmerged.rename(index=fix_index,inplace=True)
    countries = ['United States','Australia','Great Britain','Japan','New Zealand']
    Arow = dmerged.loc[countries]
    # ax = plt.axes()
    ax = Arow.plot.bar(y=["Gold_Winter","Silver_Winter","Bronze_Winter"],title="Winter Games",color=['#4671be','#eb7c3e','#a3a3a3'],rot=0)
    ax.legend(["Gold","Silver","Bronze"])
    # ax.set_position(pos='bottom')
    # ax.set_xticklabels(ax.get_xticklabels(),rotation=90)
    ax.set_aspect(aspect='auto')
    plt.show()
    
    



if __name__ == '__main__':
    dmerged = question_1()
    dmerged = question_2(dmerged)
    dmerged = question_3(dmerged)
    dmerged = question_4(dmerged)
    dmerged = question_5(dmerged)
    question_6(dmerged)
    dsorted = question_7(dmerged)
    question_8(dsorted)
    question_9(dmerged)

