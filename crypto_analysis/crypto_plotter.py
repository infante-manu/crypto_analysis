"""Handles plotting for cryptocurrency data and indicators."""

from typing import Any
import pandas as pd
import plotly.graph_objects as go

class CryptoPlotter:
    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def get_data_plot(self) -> None:
        """
        Plots the cryptocurrency data with Bollinger Bands and signals using Plotly.
        """
        fig = self.get_plot_data()
        fig.show()

    def get_portfolio_plot(self, portfolio_value: pd.Series, initial_capital: float) -> None:
        """
        Plots the investment value over time and buy/sell signals using Plotly.

        Parameters:
            portfolio_value (pd.Series): Series containing portfolio value over time.
            initial_capital (float): Initial capital used for reference in the plot.
        """
        fig = self.get_plot_portfolio(portfolio_value, initial_capital)
        fig.show()

    def get_data_plot(self) -> None:
        """
        Plots the cryptocurrency data with Bollinger Bands and signals using Plotly.
        """
        fig = go.Figure()

        # Adding Close Price
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['close'], mode='lines', name='Close Price',
                                 line=dict(color='blue', width=1.5), opacity=0.6))

        # Adding Bollinger Bands
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['upper_band'], mode='lines', name='Upper Band',
                                 line=dict(color='yellow', width=1), opacity=0.6))
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['lower_band'], mode='lines', name='Lower Band',
                                 line=dict(color='purple', width=1), opacity=0.6))

        # Fill between upper and lower band
        fig.add_trace(go.Scatter(x=self.data.index, y=self.data['upper_band'], mode='lines', line=dict(color='grey', width=0),
                                 fill='tonexty', fillcolor='rgba(128, 128, 128, 0.2)', name='Band Fill'))

        # Adding Buy and Sell signals
        if 'buy' in self.data.columns and 'sell' in self.data.columns:
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['buy'], mode='markers', name='Buy Signals',
                                     marker=dict(symbol='triangle-up', color='green', size=10)))
            fig.add_trace(go.Scatter(x=self.data.index, y=self.data['sell'], mode='markers', name='Sell Signals',
                                     marker=dict(symbol='triangle-down', color='red', size=10)))

        # Layout
        fig.update_layout(title='Bollinger Bands & RSI Trading Strategy',
                          xaxis_title='Dates',
                          yaxis_title='Price in USD',
                          hovermode='x unified')

        return fig

    def get_portfolio_plot(self, portfolio_value: pd.Series, initial_capital: float) -> None:
        """
        Plots the investment value over time and buy/sell signals using Plotly.

        Parameters:
            portfolio_value (pd.Series): Series containing portfolio value over time.
            initial_capital (float): Initial capital used for reference in the plot.
        """
        fig = go.Figure()

        # Adding Portfolio Value
        fig.add_trace(go.Scatter(x=portfolio_value.index, y=portfolio_value, mode='lines', name='Portfolio Value',
                                 line=dict(color='blue', width=1.5)))

        # Adding Initial Capital Line
        fig.add_trace(go.Scatter(x=portfolio_value.index, y=[initial_capital] * len(portfolio_value),
                                 mode='lines', name='Initial Capital',
                                 line=dict(color='green', dash='dash')))

        # Layout
        fig.update_layout(title='Backtest Portfolio Value Over Time',
                          xaxis_title='Date',
                          yaxis_title='Portfolio Value',
                          hovermode='x unified')

        return fig
    

