import pandas as pd
import numpy as np
class SignalGenerator:
    def __init__(self, data: pd.DataFrame) -> None:
        """
        Initializes the SignalGenerator with processed trading data.

        Parameters:
            data (pd.DataFrame): DataFrame containing price data with technical indicators.
        """
        self._validate_data(data)
        self.data = data

    def _validate_data(self, data: pd.DataFrame) -> None:
        """Validates that required columns exist in the data."""
        required_columns = {'close', 'upper_band', 'lower_band', 'rsi', 'over_sold', 'over_bought'}
        missing_columns = required_columns - set(data.columns)

        if missing_columns:
            raise ValueError(f"Data is missing required columns: {missing_columns}")

    def generate_signals(self) -> pd.DataFrame:
        """
        Generates buy and sell signals based on Bollinger Bands and RSI.

        Returns:
            pd.DataFrame: DataFrame with buy and sell signals.
        """
        try:
            df = self.data
            position = 0
            buy_price = []
            sell_price = []

            for i in df.index:
                # Check for valid numeric values in relevant columns
                if not pd.isna(df.loc[i, 'close']) and \
                   not pd.isna(df.loc[i, 'lower_band']) and \
                   not pd.isna(df.loc[i, 'rsi']) and \
                   not pd.isna(df.loc[i, 'upper_band']):
                    
                    if df.loc[i, 'close'] < df.loc[i, 'lower_band'] and df.loc[i, 'rsi'] < df.loc[i, 'over_sold'] and position == 0:
                        position = 1
                        buy_price.append(df['close'][i])
                        sell_price.append(np.nan)
                    elif df.loc[i, 'close'] > df.loc[i, 'upper_band'] and df.loc[i, 'rsi'] > df.loc[i, 'over_bought'] and position == 1:
                        position = 0
                        sell_price.append(df['close'][i])
                        buy_price.append(np.nan)
                    else:
                        buy_price.append(np.nan)
                        sell_price.append(np.nan)
                else:
                    raise ValueError(f"Invalid or missing data for signal calculation at index {i}")

            df['buy'] = buy_price
            df['sell'] = sell_price

            return df

        except Exception as e:
            raise RuntimeError(f"Failed to generate signals: {e}")
