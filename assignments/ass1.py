#/usr/bin/python3

import pandas as pd
from tabulate import tabulate
import matplotlib.pyplot as plt
import re

#loads csv data into a dataframe
def load_csv(csv_filename):
    dataframe = pd.read_csv(csv_filename, encoding='utf-8')
    return dataframe

 # Prints the data, prints columns and then each row
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


def print_table(df):
    print_dataframe(df,print_rows=False)
    print(tabulate(df))


#Removes the comma in the values and converts them to all a number
def cleansing(df):
    for column in df:
        df[column]= df[column].apply(str).apply(lambda x: x.replace(',',''))
        df[column] = pd.to_numeric(df[column])

    return df

#Removes the useless information after the country
def fix_index(line):
        line = re.sub(r'\(.*\)',"",line)
        line = re.sub(r'\[.*\]',"",line).strip()
        return line


#Loads the excel, make the countries as the index, rename the columns, print the first 4 dataframe
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
    print_table(dmerged)
    print_dataframe(dmerged.head(5))
    return dmerged


#Prints the first country and the countries are already the index as completed in question 1
def question_2(dmerged):
    print("*********************************************")
    print("Question 2")
    print("*********************************************")
    #index has been placed to country already in the first question
    print_dataframe(dmerged.head(1))
    return dmerged

#Removes the Rubish column
def question_3(dmerged):
    print("*********************************************")
    print("Question 3")
    print("*********************************************")
    dmerged.drop('Rubish',axis=1,inplace=True)
    print_dataframe(dmerged.head(5))
    return dmerged

#Drops all rows that have Nan in them
def question_4(dmerged):
    print("*********************************************")
    print("Question 4")
    print("*********************************************")
    dmerged.dropna(inplace=True)
    print_dataframe(dmerged.tail(10))
    return dmerged

#Prints country that contains most amount of Gold medals
def question_5(dmerged):
    print("*********************************************")
    print("Question 5")
    print("*********************************************")
    #Uses the cleansing function - converts all of the values to an integer
    dmerged = cleansing(dmerged)
    dGold=dmerged['Gold_Summer']
    dGold = dGold[:(len(dGold) - 1)]
    max_df=dGold.idxmax()
    print(str(max_df) + " contains " + str(dGold.loc[max_df]) + " Gold medals")
    return dmerged

#Prints the country with the biggest difference between summer and winter games
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

#Sorts country in descending order of the total number of medals
def question_7(dmerged):
    print("*********************************************")
    print("Question 7")
    print("*********************************************")
    dsorted = dmerged.sort_values(by='Total_Medals',axis=0,ascending=False,)
    print_table(dsorted)
    print("--------- Top 5 Rows ---------")
    print_dataframe(dsorted.head(5))
    print("--------- Bottom 5 Rows ---------")
    print_dataframe(dsorted.tail(5))
    return dsorted

#Prints out medals for winter and summer games
def question_8(dsorted):
    print("*********************************************")
    print("Question 8")
    print("*********************************************")
    dsorted.rename(index=fix_index,inplace=True)
    dftop = dsorted.head(10)
    ax= dftop.plot.barh(y=['Total_Summer','Total_Winter'],stacked=True, title='Medals for Winter and Summer Games')
    ax.legend(["Summer Games","Winter Games"])
    plt.show()

#Prints column graph for those respective countries
def question_9(dmerged):
    print("*********************************************")
    print("Question 9")
    print("*********************************************")
    dmerged.rename(index=fix_index,inplace=True)
    countries = ['United States','Australia','Great Britain','Japan','New Zealand']
    Arow = dmerged.loc[countries]
    ax = Arow.plot.bar(y=["Gold_Winter","Silver_Winter","Bronze_Winter"],title="Winter Games",color=['#4671be','#eb7c3e','#a3a3a3'],rot=0)
    ax.legend(["Gold","Silver","Bronze"])
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

