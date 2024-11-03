"""Generates trading signals based on technical indicators."""

import pandas as pd
import numpy as np

class SignalGenerator:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def generate_signals(self) -> pd.DataFrame:
        """
        Generates buy and sell signals based on Bollinger Bands and RSI.
        Returns:
            pd.DataFrame: DataFrame with buy and sell signals.
        """
        df = self.data
        position = 0
        buy_price = []
        sell_price = []

        for i in df.index:
            if (df.loc[i, 'close'] < df.loc[i, 'lower_band'] and 
                df.loc[i, 'rsi'] < df.loc[i, 'over_sold'] and 
                position == 0):
                position = 1
                buy_price.append(df['close'][i])
                sell_price.append(np.nan)
            elif (df.loc[i, 'close'] > df.loc[i, 'upper_band'] and 
                  df.loc[i, 'rsi'] > df.loc[i, 'over_bought'] and 
                  position == 1):
                position = 0
                sell_price.append(df['close'][i])
                buy_price.append(np.nan)
            else:
                buy_price.append(np.nan)
                sell_price.append(np.nan)

        df['buy'] = buy_price
        df['sell'] = sell_price
        
        return df
