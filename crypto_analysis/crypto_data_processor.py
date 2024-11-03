from typing import Any
import pandas as pd
from crypto_analysis.kraken_api_handler import KrakenAPIHandler

class CryptoDataProcessor:
    """Processes and analyzes cryptocurrency data."""
    
    def __init__(self, pair : str, interval : int = 1440, oversold : int = 30, overbought : int = 70) -> None:
        self.kraken_api_handler = KrakenAPIHandler()
        self.pair = pair
        self.interval = interval
        self.data = None
        self.oversold = oversold
        self.overbought = overbought
        self.fetch_data()

    def fetch_data(self):
        self.data = self.kraken_api_handler.fetch_ohlc_data(self.pair, self.interval)
    
    def get_processed_data(self) -> pd.DataFrame:
        df = self.data
        df = self.calculate_bollinger_bands(df)
        df = self.calculate_rsi(df)
        df = df.dropna(subset = ['moving_avg', 'moving_std_dev', 'upper_band', 'lower_band', 'rsi'])
        return df

    def calculate_bollinger_bands(self, df : pd.DataFrame(), column: str = 'close', window: int = 20, num_std_dev: int = 2) -> pd.DataFrame:
        """
        Calculate Bollinger Bands for a given DataFrame with closing prices.
        
        Parameters:
        column (str): Name of the column to calculate Bollinger Bands on (default: 'close')
        window (int): Number of periods for the moving average and standard deviation (default: 20)
        num_std_dev (int): Number of standard deviations for the bands (default: 2)
        
        Returns:
        pd.DataFrame: Original DataFrame with added columns for Bollinger Bands
        """
        # Calculate rolling mean and standard deviation
        temp = df.copy()
        df = temp
        df['moving_avg'] = df[column].rolling(window=window).mean()
        df['moving_std_dev'] = df[column].rolling(window=window).std()

        # Calculate Upper and Lower Bollinger Bands
        df['upper_band'] = df['moving_avg'] + (df['moving_std_dev'] * num_std_dev)
        df['lower_band'] = df['moving_avg'] - (df['moving_std_dev'] * num_std_dev)

        return df
    
    def calculate_rsi(self, df, column: str = 'close', period: int = 14) -> pd.DataFrame:
        """
        Calculate the Relative Strength Index (RSI) for a given DataFrame.

        Parameters:
        - column (str): The column name to calculate RSI on (default: 'close').
        - period (int): The lookback period for RSI calculation (default: 14).

        Returns:
        - pd.DataFrame: DataFrame with an additional 'rsi' column.
        """
        temp = df.copy()
        df = temp
        delta = df[column].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()

        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))
        df['over_sold'] = self.oversold
        df['over_bought'] = self.overbought

        return df


if __name__ == '__main__':
    # Example usage
    processor = CryptoDataProcessor(pair='ETHUSD') 
    processed_data = processor.get_processed_data()
    print(processed_data)