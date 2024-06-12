import pandas as pd
import numpy as np
from ta.utils import dropna
from ta.volume import MFIIndicator


def mfi_index(dataframe):
    dataframe = dropna(dataframe)
    dataframe = dataframe.set_index(pd.DatetimeIndex(dataframe['Date'].values))
    indicator_mfi = MFIIndicator(high=dataframe['High'], low=dataframe['Low'], close=dataframe['Close'],
                                 volume=dataframe['Volume'], window=14, fillna=True)

    return indicator_mfi.money_flow_index()