#!/usr/bin/env python
# coding: utf-8


import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math 
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM


class LstmPrediction:

    def __init__(self, forecast_days: int, input_days: int, stock_name):
        self.input_days = input_days
        self.forecast_days = forecast_days
        self.stock_name = stock_name
        self.data = self.__load_data__()
        self.model, self.prediction, self.scaler = self.__train__()

    def __load_data__(self):

        # Read Data =
        df = pd.read_csv('F:/Projects/Trader/TraderV001/Data/' + self.stock_name + '.csv')
        df.set_index(pd.DatetimeIndex(df['<DATE>'].values))
        return df

    def __train__(self):

        dataset = self.data.filter(['<CLOSE>'])

        # print('this is dataset scaled\' shape: ', dataset.shape)
        # Scale Dataset
        training_data_len = math.ceil(len(dataset)*0.8)
        scaler = MinMaxScaler(feature_range=(0, 1))
        print('dataset shape is:', dataset.shape)
        scaled_data = scaler.fit_transform(dataset.values)

        # Create Training Data
        training_data = scaled_data[0:training_data_len, :]
        x_train = []
        y_train = []
        n = self.input_days

        for i in range(n, len(training_data)-10):
            x_train.append(training_data[i-n:i, 0])
            y_train.append(training_data[i:i + 10, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # Create Neural Network
        model = Sequential()
        model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
        model.add(LSTM(50, return_sequences=False))
        model.add(Dense(25))
        model.add(Dense(10))

        # Compile loss function
        model.compile(loss='mean_squared_error', optimizer='adam')

        # Train model
        model.fit(x_train, y_train, epochs=1, batch_size=4)

        # Provide Data for prediction
        prediction_data = scaled_data[:, :]

        x_predict = []

        for i in range(n, len(prediction_data)-9):
            x_predict.append(prediction_data[i-n: i, 0])

        x_predict = np.array(x_predict)
        x_predict = np.reshape(x_predict, (x_predict.shape[0], x_predict.shape[1], 1))

        # Predict
        prediction = model.predict(x_predict)
        prediction = scaler.inverse_transform(prediction)
        prediction = prediction[:, 1]

        temp = np.zeros(n+9)
        prediction = np.append(temp, prediction)

        pd.Series(prediction, index=self.data.index)

        return model, prediction, scaler

    def get_prediction(self):
        return self.prediction

    def get_model(self):
        return self.model

    def predict(self, data):

        data = np.array(data)
        data = np.reshape(data, (data.shape[0], 1))
        x_data = self.scaler.transform(data)
        x_data = np.reshape(x_data, (1, x_data.shape[0], 1))

        prediction = self.model.predict(x_data)

        return self.scaler.inverse_transform(prediction)

    def get_input_days(self):
        return self.input_days






