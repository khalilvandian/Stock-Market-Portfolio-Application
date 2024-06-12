from Stock import Stock
from Action import Action
from abc import ABC, abstractmethod
import InfoExtractor as ie
from TechnicalAnalysis import TechnicalAnalysis as TA
import random
import backtrader as bt
import Prediction
import numpy as np
from keras.models import sequential
from sklearn.preprocessing import MinMaxScaler
from lstm import LstmPrediction


class Strategy(ABC):

    @abstractmethod
    def signal(self):
        pass


class highest_rate(Strategy):

    def __init__(self):
        self.name = "highest rate"

    def __calculate(self):
        self.act = Action("buy", Stock("مدیریت"), "3000")
        return self.act

    def signal(self):
        self.__calculate()
        return self.act


class three_day_highest(Strategy):

    def __init__(self):
        self.name = "three day highest"

    def __calculate(self):
        candids = ie.highest_profit_rate()

        self.act = []
        for stock in candids:
            self.act.append(Action(random.choice(['buy', 'sell']), stock, self.__action_weight()))

    def __action_weight(self):
        return random.randint(2000, 5000)

    def signal(self):
        self.__calculate()
        return self.act


class SimpleStrategy(Strategy):

    def __init__(self, data):
        self.data = data
        self.signal = self.__calculate()

    def __calculate(self):
        ta_object = TA(self.data)
        return ta_object.rsi_signal()

    def signal(self):
        return self.signal()


class TestStrategy(bt.Strategy):


    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        # self.rsi = bt.indicators.RelativeStrengthIndex()
        # self.lr = Prediction.PredictWithLR(5)

        # Keep a reference to the "close" line in the data[0] dataseries
        self.datapred = self.datas[0].prediction

        # To keep track of pending orders
        self.order = None
        self.bar_executed = None

    # def notify_order(self, order):
    #     if order.status in [order.Submitted, order.Accepted]:
    #         # Buy/Sell order submitted/accepted to/by broker - Nothing to do
    #         return
    #
    #     # Check if an order has been completed
    #     # Attention: broker could reject order if not enough cash
    #     if order.status in [order.Completed]:
    #         if order.isbuy():
    #             self.log('BUY EXECUTED, %.2f' % order.executed.price)
    #         elif order.issell():
    #             self.log('SELL EXECUTED, %.2f' % order.executed.price)
    #
    #         self.bar_executed = len(self)
    #
    #     elif order.status in [order.Canceled, order.Margin, order.Rejected]:
    #         self.log('Order Canceled/Margin/Rejected')
    #
    #     # Write down: no pending order
    #     self.order = None

    def next(self):

        self.log('prediction is: %.2f' % self.datapred[0])

        #         self.log('buy point')
        #         # we buy at this part
        #         self.log('buy CREATE, %.2f' % self.dataclose[0])
        #         # Keep track of the created order to avoid a 2nd order
        #         self.order = self.buy()
        #
        #         self.bar_executed = len(self)
        #
        #
        # else:
        #
        #     if len(self) >= self.bar_executed + 5:
        #         # BUY BUUUUUUUUY!
        #         self.log('sell CREATE, %.2f' % self.dataclose[0])
        #         self.order = self.sell()


class MachineBased(bt.Strategy):

    params = (
        ('min_profit_limit', 0.05),
        ('max_profit_limit', 0.10),
        ('loss_limit', 0.05),
        ('days_forecasted', 10)
    )

    __model: sequential
    __forecast_days: int
    __scaler1: MinMaxScaler
    __lstm_obj : LstmPrediction

    @classmethod
    def set_model(cls, model: sequential):
        cls.__model = model

    @classmethod
    def set_forecast_days(cls, days: int):
        cls.__forecast_days = days

    @classmethod
    def set_scaler(cls, scaler: MinMaxScaler):
        cls.__scaler1 = scaler

    @classmethod
    def set_lstm_obj(cls, lstm_obj: LstmPrediction):
        cls.lstm_obj = lstm_obj



    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):

        self.rsi = bt.indicators.RelativeStrengthIndex()
        self.lr = Prediction.PredictWithLR(5)

        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None
        self.bar_executed = None

    def next(self):


        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f , RSI : %.2f' % (self.dataclose[0], self.rsi[0]))

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Prediction class will provide this variable with predicted value for nth day
        if len(self) > 59:
            pred_data = self.provide_data_for_prediction()
            prediction = self.lstm_obj.predict(pred_data)

        # prediction = machine.predict(days (current + 1 => current + 14)

        # Check if we are in the market
        if not self.position and len(self) > 59:

            # Check if predictions pass or reach the profit limit, if so order a BUY.
            flag = False
            for x in prediction[0]:
                if (x - self.dataclose[0]) >= (self.params.max_profit_limit * self.dataclose[0]):
                    flag = True
                    # print('this is close of the day', self.dataclose[0])
                    # print('this is prediction of the day', prediction[0])

            if flag and len(self) > 59:
                self.buy()
                # self.log('BUY CREATE, %.2f' % self.dataclose[0])
                self.bar_executed = len(self)

        # Already in the market ... we might sell
        elif self.position:

            x = self.position.price  # price the stock is bought

            # If the profit has reached the limit order a SELL.
            if self.dataclose[0] >= (x * (1 + self.params.max_profit_limit)):
                self.sell()
                # self.log('SELL CREATE, %.2f ' % self.dataclose[0])

            # If we have lost more than the limit set, order a SELL.
            elif self.dataclose[0] <= (x * (1 - self.params.loss_limit)):
                self.sell()
                # self.log('SELL CREATE, %.2f' % self.dataclose[0])

            #
            elif len(self) >= 14 + self.bar_executed:
                self.sell()
                # self.log('SELL CREATE, %.2f' % self.dataclose[0])

    def apply(self):

        # TODO: this function will apply the strategy and provide the user
        #  with appropriate action corresponding with the strategy at hand.
        data = self.provide_data_for_prediction()
        prediction = self.lstm_obj.predict(data)
        sell_flag = False

        for x in prediction[0]:
            if (x - self.dataclose[0]) >= (self.params.max_profit_limit * self.dataclose[0]):
                return Action('buy', Stock('Bama'), self.env.broker.getvalue())

            if (self.dataclose[0]) <= ((1 - self.params.loss_limit) * self.dataclose[0]):
                sell_flag = True

        if (sell_flag):
            return Action('sell', Stock('Bama'), self.env.broker.getvalue())

        return Action('nothing', Stock('Bama'), 0)


    def provide_data_for_prediction(self):

        if len(self.dataclose) >= 60:

            data = self.dataclose.get(size=self.lstm_obj.get_input_days())
            return data

        return False




