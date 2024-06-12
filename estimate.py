import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
from crawlscrape import get_stocks
plt.style.use('fivethirtyeight')


def LSTM_prediction(stock_name):

    df = get_stocks(stock_name)
    df = df.set_index('date')
    data = df.filter(['close'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) * 0.8)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    training_data = scaled_data[0:training_data_len, :]
    xtrain = []
    ytrain = []
    n = 50
    for i in range(n, len(training_data)):
        xtrain.append(training_data[i - n:i, 0])
        ytrain.append(training_data[i, 0])

    xtrain, ytrain = np.array(xtrain), np.array(ytrain)
    xtrain = np.reshape(xtrain, (xtrain.shape[0], xtrain.shape[1], 1))
    model = Sequential()
    model.add(LSTM(100, return_sequences=True, input_shape=(xtrain.shape[1], 1)))
    model.add(LSTM(100, return_sequences=False))
    model.add(Dense(50))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(xtrain, ytrain, epochs=15, batch_size=5)
    test_data = scaled_data[training_data_len - n:, :]
    xtest = []
    ytest = dataset[training_data_len:, :]
    for i in range(n, len(test_data)):
        xtest.append(test_data[i - n: i, 0])

    xtest = np.array(xtest)
    xtest = np.reshape(xtest, (xtest.shape[0], xtest.shape[1], 1))
    prediction = model.predict(xtest)
    prediction = scaler.inverse_transform(prediction)
    # root mean squared error
    rmse = np.sqrt(np.mean((prediction - ytest) ** 2))
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['prediction'] = prediction
    newdf = data[-50:].values
    scalednewdf = scaler.transform(newdf)
    xtest = []
    xtest.append(scalednewdf)
    xtest = np.array(xtest)
    xtest = np.reshape(xtest, (xtest.shape[0], xtest.shape[1], 1))
    pred = model.predict(xtest)
    pred = scaler.inverse_transform(pred)
    result_dict = {"prediction": pred, "error": rmse}

    return result_dict, model
