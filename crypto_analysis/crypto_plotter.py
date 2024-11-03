"""Handles plotting for cryptocurrency data and indicators."""

from typing import Any
import pandas as pd
import matplotlib.pyplot as plt

class CryptoPlotter:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def plot_data(self) -> None:
        """
        Plots the cryptocurrency data with Bollinger Bands and signals.
        """
        fig, ax = plt.subplots(figsize=(16, 8))
        plt.title('Bollinger Bands & RSI Trading Strategy')
        plt.ylabel('Price in USD')
        plt.xlabel('Dates')

        ax.plot(self.data['close'], label='Close Price', alpha=0.25, color='blue')
        ax.plot(self.data['upper_band'], label='Upper Band', alpha=0.25, color='yellow')
        ax.plot(self.data['lower_band'], label='Lower Band', alpha=0.25, color='purple')
        ax.fill_between(self.data.index, self.data['upper_band'], self.data['lower_band'], color='grey', alpha=0.2)
        
        # Ensure Buy and Sell columns exist in the DataFrame
        if 'buy' in self.data.columns and 'sell' in self.data.columns:
            ax.scatter(self.data.index, self.data['buy'], label='buy', alpha=1, marker='^', color='green')
            ax.scatter(self.data.index, self.data['sell'], label='Sell', alpha=1, marker='v', color='red')

        plt.legend()
        plt.show()

    def plot_results(self, portfolio_value: pd.Series, initial_capital: float) -> None:
        """
        Plots the investment value over time and buy/sell signals.

        Parameters:
            portfolio_value (pd.Series): Series containing portfolio value over time.
            initial_capital (float): Initial capital used for reference in the plot.
        """
        fig, ax = plt.subplots(figsize=(14, 7))
        
        plt.title('Backtest Portfolio Value Over Time')
        plt.xlabel('Date')
        plt.ylabel('Portfolio Value')
        
        ax.plot(portfolio_value, label='Portfolio Value', color='blue')
        ax.axhline(y=initial_capital, color='green', linestyle='--', label='Initial Capital')

        plt.legend()
        plt.show()
