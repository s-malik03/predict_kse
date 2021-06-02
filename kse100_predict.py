import matplotlib.pyplot as plt
from matplotlib import style
import pandas
import numpy
from datetime import datetime
import pickle
from sklearn import preprocessing

style.use('ggplot')

dataframe = pandas.read_csv('stock-exchange-kse-100pakistan.csv', index_col=0)
dataframe.reset_index(drop=True)
dataframe = dataframe.replace(',', '', regex=True)
dataframe['Open'] = pandas.to_numeric(dataframe['Open'])
dataframe['Close'] = pandas.to_numeric(dataframe['Close'])
dataframe['High'] = pandas.to_numeric(dataframe['High'])
dataframe['Low'] = pandas.to_numeric(dataframe['Low'])
dataframe['Change'] = pandas.to_numeric(dataframe['Change'])
dataframe['Volume'] = pandas.to_numeric(dataframe['Volume'])
dataframe['Forecast'] = numpy.nan
dataframe["HL_PDIFF"] = (dataframe["High"] - dataframe["Low"]) / dataframe["Low"]
dataframe["OC_PDIFF"] = (dataframe["Open"] - dataframe["Close"]) / dataframe["Close"]

pred_data = numpy.array(dataframe[['Volume', 'HL_PDIFF', 'OC_PDIFF', 'Close']].iloc[0])
numpy.set_printoptions(suppress=True)

dataframe.iloc[0, dataframe.columns.get_loc('Forecast')] = dataframe.iloc[0, dataframe.columns.get_loc('Close')]
dataframe[[col for col in dataframe.columns]] = dataframe[[col for col in dataframe.columns]].shift(1)

pickle_in = open('kse100_save.pickle', 'rb')
model = pickle.load(pickle_in)

pickle_in = open('kse100_scaler.pickle', 'rb')
scaler = pickle.load(pickle_in)

pred = model.predict(scaler.transform([pred_data]))

print(pred[0])

dataframe.iloc[0] = [numpy.nan for _ in range(len(dataframe.columns) - 3)] + [pred[0]] + [numpy.nan] + [numpy.nan]
dataframe.index = pandas.to_datetime(dataframe.index, format="%d-%b-%y")

dataframe['Forecast'][:30].plot()
dataframe['Close'][:30].plot()

plt.legend()
plt.xlabel('Date')
plt.ylabel('Value')
plt.savefig('prediction_'+datetime.now().strftime("%d-%b-%y")+'.png')
plt.show()
