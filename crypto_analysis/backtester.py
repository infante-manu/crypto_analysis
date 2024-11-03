import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Backtester:
    def __init__(self, data: pd.DataFrame, initial_capital: float = 10000) -> None:
        """
        Initializes the Backtester with trading data and initial capital.
        
        Parameters:
            data (pd.DataFrame): DataFrame containing trading signals and price data.
            initial_capital (float): Starting capital for the backtest.
        """
        self.data = data
        self.initial_capital = initial_capital
        self.current_capital = self.initial_capital
        self.positions = []  # To keep track of positions taken
        self.trades = []  # To keep track of trade results
        self.portfolio_values = pd.Series(dtype=float)  # To store portfolio value over time

    def run_backtest(self) -> pd.DataFrame:
        """
        Runs the backtest on the trading signals and computes results.
        Returns:
            pd.DataFrame: A DataFrame with the results of the backtest.
        """
        position = 0  # Current position (1 for long, 0 for no position)
        entry_price = 0  # Price at which the position was entered
        
        for index, row in self.data.iterrows():
            # Buy Signal
            if not pd.isna(row['buy']) and position == 0:
                position = 1  # Enter position
                entry_price = row['buy']
                self.positions.append(('buy', row['buy'], index))

            # Sell Signal
            elif not pd.isna(row['sell']) and position == 1:
                position = 0  # Exit position
                profit = row['sell'] - entry_price
                self.current_capital += profit
                self.trades.append((entry_price, row['sell'], profit, index))
                self.positions.append(('sell', row['sell'], index))

            # Store the portfolio value
            self.portfolio_values.at[index] = self.current_capital

        results_df = self.calculate_metrics()
        return results_df

    def calculate_metrics(self) -> pd.DataFrame:
        """
        Calculate Sharpe Ratio, Annual Return, and Max Drawdown.
        """
        # Calculate returns
        returns = self.portfolio_values.pct_change().dropna()
        
        # Sharpe Ratio
        sharpe_ratio = (returns.mean() / returns.std()) * np.sqrt(252)  # Annualize

        # Normalized Annual Return
        annual_return = (self.portfolio_values.iloc[-1] / self.initial_capital - 1) * 100

        # Maximum Drawdown
        drawdown = self.portfolio_values.expanding().max() - self.portfolio_values
        max_drawdown = (drawdown.max() / self.portfolio_values.expanding().max()).iloc[-1] * 100

        # Create results DataFrame
        results = {
            'Initial Capital': [self.initial_capital],
            'Final Capital': [self.current_capital],
            'Total Trades': [len(self.trades)],
            'Winning Trades': [len([trade for trade in self.trades if trade[2] > 0])],
            'Losing Trades': [len([trade for trade in self.trades if trade[2] < 0])],
            'Total Profit': [self.current_capital - self.initial_capital],
            'Sharpe Ratio': [sharpe_ratio],
            'Normalized Annual Return (%)': [annual_return],
            'Max Drawdown (%)': [max_drawdown]
        }

        return pd.DataFrame(results)

    def get_portfolio_values(self) -> pd.Series:
        """
        Returns the portfolio values over time.

        Returns:
            pd.Series: A Series containing portfolio values indexed by date.
        """
        return self.portfolio_values
