import Strategies
from Action import Action
import pandas as pd
import backtrader as bt
import Strategy
import lstm
import datetime
from Action import Action
import backtrader.analyzers as btanalyzers


class Recommender:

    def __init__(self):
        self.strategies = []

    def __add_strategy(self):
        self.strategies[0] = Strategies.highest_rate()

    def  plan(self):
        a = Strategies.three_day_highest()
        return a.signal()


class RecommenderBt:

    def __init__(self, owner_account_name: str, stock_name: str, forecast_days: int):
        self.owner_account_name = owner_account_name
        self.stock_name = stock_name
        self.forecast_days = forecast_days

        # TODO: File address should become generic
        self._file_address = 'F:/Projects/Trader/TraderV001/Data/' + stock_name + '.csv'

        self.stockData = self.__load_stock_data()
        self.lstm_obj = self.__initialize_lstm_model()
        # self.predictions = self.__predict()
        self.strategy = self.__initialize_cerebro()
        self.actions = self.__produce_actions()

    def __initialize_lstm_model(self):
        lstm_obj = lstm.LstmPrediction(forecast_days=self.forecast_days, input_days=60, stock_name=self.stock_name)
        return lstm_obj

    # TODO: provides data needded for prediction
    def __provide_data_for_prediction(self):
        return 0

    # TODO: Creates a variable containing all the predictions achieved by the lstm model,
    #  series variable is being returned that is indexed by date
    def __predict(self):
        data = self.__provide_data_prediction()
        predictions = self.lstm_model.predict(data)
        return predictions

    # TODO: Initialize CEREBRO, backtest strategies, return Instance of Strategy
    def __initialize_cerebro(self):

        # Create a cerebro entity
        self.cerebro = bt.Cerebro()

        # Add a strategy
        # Strategy.MachineBased.set_model(self.lstm_obj.get_model())
        # Strategy.MachineBased.set_forecast_days(self.forecast_days)
        Strategy.MachineBased.set_lstm_obj(self.lstm_obj)

        self.cerebro.addstrategy(Strategy.MachineBased)

        # Datas are in a subfolder of the samples. Need to find where the script is
        # because it could have been called from anywhere
        # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
        # datapath = os.path.join(modpath, '../TraderV001/Data/S_Isf..Oil.Ref.Co..csv')

        # Create a Data Feed
        data = bt.feeds.PandasData(
            dataname=self.stockData,
            open=10,
            close=5,
            high=3,
            low=4,
            volume=7,
            openinterest=8,
            fromdate=datetime.datetime(2020, 1, 1)
        )

        # Add the Data Feed to Cerebro
        self.cerebro.adddata(data)

        # Set our desired cash start
        self.cerebro.broker.setcash(100000.0)

        # cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

        # Print out the starting conditions
        print('Starting Portfolio Value: %.2f' % self.cerebro.broker.getvalue())

        self.cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

        # Run over everything
        strat = self.cerebro.run()
        print('Final Portfolio Value: %.2f' % self.cerebro.broker.getvalue())
        self.cerebro.plot()
        return strat[0]
        # print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
        # strat[0].next()
        # cerebro.plot()

    # TODO: Produce list of actions recommended for the user in next n days
    def __produce_actions(self):

        # TODO: Provide the function with appropriate data so that the strategy would produce actions recommended
        actions = self.strategy.apply()
        return actions

    def __load_stock_data(self):
        df = pd.read_csv(filepath_or_buffer=self._file_address)
        df = df.set_index(pd.DatetimeIndex(df['<DATE>'].values))
        return df

    def get_actions(self):
        self.actions.get_action()

    def get_analysis(self):
        analysis = self.strategy.analyzers.mysharpe.get_analysis()
        print('strategy analysis result is: ', analysis)



