import pandas as pd
from ta.utils import dropna
from ta.volume import MFIIndicator


class TechnicalAnalysis:

    def __init__(self, data: pd.DataFrame):
        self.data = dropna(data)
        mfi_signal = str

    def __calculate_mfi(self):
        indicator_mfi = MFIIndicator(self.data['<HIGH>'], self.data['<LOW>'], self.data['<CLOSE>'], self.data['<VOL>'], window=14)
        return indicator_mfi.money_flow_index()

    def rsi_signal(self):
        df = self.__calculate_mfi()
        last_day = df['<CLOSE>'].iloc[-1]

        if last_day >= 50:
            self.mfi_signal = 'sell'

        else:
            self.mfi_signal = 'buy'

        return self.mfi_signal

    def get_rsi_index(self):
        return self.__calculate_mfi()


