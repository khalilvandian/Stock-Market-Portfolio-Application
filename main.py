from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import logging
from Account import Account
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import Indicators as ind
import datetime  # For datetime objects
import os.path  # To manage paths
import sys
import backtrader as bt
import Strategy
import backtrader.analyzers as btanalyzers
# from Prediction import PredictWithLR as pdlr
# from estimate import LSTM_prediction
# import crawlscrape as cs
from Test import Test
from sklearn.preprocessing import MinMaxScaler
from lstm import LstmPrediction
import pickle
np.set_printoptions(threshold=sys.maxsize)

if __name__ == '__main__':
    logging.basicConfig(filename='F:/Projects/Trader/TraderV001/log.log', level=logging.ERROR,
                        filemode='w')
    my_account = Account('babak', 'babak', '1234')
    my_account.get_machine_plan()
    sys.stdout.close()

    # input = input('enter a value: ')
    # print('your value is: ', input)

#
#
#     df = pd.read_csv(filepath_or_buffer='../TraderV001/Data/Bama.csv')
#     df = df.set_index(pd.DatetimeIndex(df['<DATE>'].values))
#     df['<prediction>'] = df['<CLOSE>'] * 0
#
#     scaler = MinMaxScaler(feature_range=(0, 1))ح
#     temp = scaler.fit([df['<CLOSE>'].values])
#
#     # Setup model
#     lstm_obj = LstmPrediction(10, 60, 'Bama')
#
#     # Create a cerebro entity
#     cerebro = bt.Cerebro()
#
#     # Add a strategy
#     Strategy.MachineBased.set_model(lstm_obj.get_model())
#     Strategy.MachineBased.set_forecast_days(10)
#     Strategy.MachineBased.set_scaler(scaler)
#     Strategy.MachineBased.set_lstm_obj(lstm_obj)
#
#     cerebro.addstrategy(Strategy.MachineBased)
#
#     # Datas are in a subfolder of the samples. Need to find where the script is
#     # because it could have been called from anywhere
#     # modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
#     # datapath = os.path.join(modpath, '../TraderV001/Data/S_Isf..Oil.Ref.Co..csv')
#
#     # Create a Data Feed
#     data = bt.feeds.PandasData_plusPred(
#         dataname=df,
#         open='<OPEN>',
#         close=5,
#         high=3,
#         low=4,
#         volume=7,
#         openinterest=8,
#         prediction='<PREDICTION>',
#         fromdate=datetime.datetime(2015, 1, 1)
#         )
#
#     # Add the Data Feed to Cerebro
#     cerebro.adddata(data)
#
#     # Set our desired cash start
#     cerebro.broker.setcash(100000.0)
#
#     # cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')
#
#     # Print out the starting conditions
#     print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
#
#     # Run over everything
#     strat = cerebro.run()
#     print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
#
#     # print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis())
#     # strat[0].next()
#     cerebro.plot()
#
#     with open('Data/strategy', 'wb') as strategy_file:
#         pickle.dump(strat, strategy_file)


















# df = df.set_index(pd.DatetimeIndex(df['Date'].values))



# df = df.head(500)
# fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1)
# ax1.plot(df['Close'], label=['close price'])
# ax2.plot(ind.mfi_index(df), label=['MFI'])
# ax2.axhline(20, linestyle='--', color='r')
# ax2.axhline(80, linestyle='--', color='r')
# plt.show()

# print(ind.mfi_index(df))
# plt.style.use('fivethirtyeight')
# df = df.set_index(pd.DatetimeIndex(df['<DATE>'].values))
# plt.figure(figsize=(30, 10))
# plt.plot(df['<CLOSE>'])
# plt.show()


# newAccnt = Account("babak", "babak", "123")
# newAccnt.get_plan()


# lst = [['hi', 'bye', 123], [2, 2, 8]]
# data = dFrame(lst, columns=['first', 'second', 'third'])
# print(data, "\n \n")
# for index, value in a.iteritems():
#     print(index)
# for index, row in a.iterrows():
#     print(row['c1'], row['c2'])

# print(a)
# a["change"] = a["closing value"] - a["opening value"]
# print(a)
# b = a.groupby(['name'])['change'].sum().sort_values(axis=0, ascending=False)
# print(b.head(3))

# print(a[a["name"] == "مدیریت"])