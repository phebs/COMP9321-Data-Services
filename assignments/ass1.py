#/usr/bin/python3

#loads csv data into a dataframe
def load_csv(csv_filename):
    dataframe = pd.read_csv(csv_filename, encoding='utf-8')
    return dataframe


def question_1():
	df1 = pd.read_csv('Olympics_dataset1.csv', index_col=0, skiprows=1)
	df2 = pd.read_csv('Olympics_dataset2.csv', index_col=0, skiprows=1)
	df1.head(5)



if __name__ == '__main__':
	question_1()