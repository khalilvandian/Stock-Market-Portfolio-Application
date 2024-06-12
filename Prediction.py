import numpy as np
import pandas as pd
from sklearn.svm import SVR
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


class PredictWithLR:

    def __init__(self, forecast: int):
        self.data = pd.read_csv(filepath_or_buffer='Data/S_Isf..Oil.Ref.Co. (1).csv')
        self.mylr = self.__fit(forecast)

    def __fit(self, forecast: int):
        df = self.data[['<CLOSE>']]
        df['<PREDICTION>'] = df[['<CLOSE>']].shift(-forecast)

        x = np.array(df.drop(['<PREDICTION>'], axis=1))
        x = x[:-forecast]
        y = np.array(df['<PREDICTION>'])
        y = y[:-forecast]

        xtrain, xtest, ytrain, ytest = train_test_split(x, y, test_size=0.2)

        mylr = LinearRegression()
        mylr.fit(xtrain, ytrain)
        return mylr

    def get_lr_predictions(self, close_price):

        result = self.mylr.predict(close_price)
        return result
