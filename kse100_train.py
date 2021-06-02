import pandas
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pickle
import numpy


# Load data from csv and remove commas in numbers, converting them to numeric values

dataframe = pandas.read_csv('stock-exchange-kse-100pakistan.csv')
dataframe = dataframe.replace(',', '', regex=True)
dataframe['Open'] = pandas.to_numeric(dataframe['Open'])
dataframe['Close'] = pandas.to_numeric(dataframe['Close'])
dataframe['High'] = pandas.to_numeric(dataframe['High'])
dataframe['Low'] = pandas.to_numeric(dataframe['Low'])
dataframe['Change'] = pandas.to_numeric(dataframe['Change'])
dataframe['Volume'] = pandas.to_numeric(dataframe['Volume'])

# Shift closing values 1 day back to become a label for each set of features

dataframe['label'] = dataframe['Close'].shift(1)
dataframe.dropna(inplace=True)

# Create new features of percentage difference between High and Low, and Open and Close

dataframe["HL_PDIFF"] = (dataframe["High"] - dataframe["Low"]) / dataframe["Low"]
dataframe["OC_PDIFF"] = (dataframe["Open"] - dataframe["Close"]) / dataframe["Close"]

scaler = preprocessing.StandardScaler()

# remove unnecessary features and scale features

dataframe = dataframe[['Date', 'Volume', 'HL_PDIFF', 'OC_PDIFF', 'Close', 'label']]
x = numpy.array(scaler.fit_transform(dataframe.drop(['label', 'Date'], axis=1).astype(float)))
y = numpy.array(dataframe['label'])

# split data into 80% train and 20% test

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# initialize and train linear regression model

change_model = LinearRegression()
change_model.fit(x_train, y_train,)
print(change_model.score(x_test, y_test,))

with open('kse100_save.pickle', 'wb') as save:
    pickle.dump(change_model, save)

with open('kse100_scaler.pickle','wb') as save:
    pickle.dump(scaler, save)
