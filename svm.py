from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from crawlscrape import get_stocks
plt.style.use("fivethirtyeight")


def SVM_prediction(stock_name):
    df = get_stocks(stock_name)
    t=20 #the number of data used
    # df=df.set_index('Date')
    #erorfindingdateprice=(df.tail(2).loc[:,'close']).head(1)
    Actual_price= df.tail(1).loc[:,'close']#for the last day
    df = df.tail(t)

    df = df.head(len(df) - 1)
    days = list()
    close_prices = list()
    df_close = df.loc[:, 'close']
    for d in range(len(df)):
        days.append([d])
    for c in df_close:
        close_prices.append(float(c))

    lin_svr = SVR(kernel='linear', C=1000.0)
    lin_svr.fit(days, close_prices)
    # poly
    poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
    poly_svr.fit(days, close_prices)
    # rbf
    rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.85)
    rbf_svr.fit(days, close_prices)
    day = [[t-1]] #all days except the lasy day are trained
    #predicting the last day which we already have the actual price
    rbf = rbf_svr.predict(day)
    poly = poly_svr.predict(day)
    lin = lin_svr.predict(day)

    #error rate for the last day
    ERrbf=((rbf - Actual_price)/Actual_price)
    ERpoly=((poly - Actual_price) /Actual_price)
    ERlin=((lin - Actual_price) /Actual_price)

    #now we train all days to predict next day
    rbf=rbf_svr.predict([[t]])
    poly=poly_svr.predict([[t]])
    lin=lin_svr.predict([[t]])

    #print('rbf predicts the price:', rbf)
    #print('poly predicts the price:', poly)
    #print('lin predicts the price:', lin)

    result_dict = {"rbf": float(rbf),'rbferror': float(ERrbf), "lin": float(lin),'linerror': float(ERlin), "ply": float(poly),'polyerror': ERpoly}

    cj=pd.DataFrame(
        [(round(float(rbf),2), round(float(ERrbf),2)),(round(float(poly),2), round(float(ERpoly),2)),(round(float(lin),2), round(float(ERlin),2))],
        index=('rbf','ply','lin'),
        columns=('Predic','Error')
        )
    return cj
