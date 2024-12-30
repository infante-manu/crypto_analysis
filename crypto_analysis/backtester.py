import numpy as np
import pandas as pd

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
        self.positions = []  # Stores each position taken in the backtest
        self.trades = []     # Stores each trade's result
        self.portfolio_values = pd.Series(dtype=float)  # Tracks portfolio values over time

    def run_backtest(self) -> pd.DataFrame:
        """Runs the backtest on the trading signals and computes results."""
        position = 0
        entry_price = 0

        for index, row in self.data.iterrows():
            # Handle buy and sell signals
            if self._is_buy_signal(row, position):
                position, entry_price = self._enter_position(row, index)
            elif self._is_sell_signal(row, position):
                position = 0
                self._exit_position(entry_price, row, index)

            # Store portfolio value over time
            self._update_portfolio_value(index)

        return self.calculate_metrics()

    def _is_buy_signal(self, row: pd.Series, position: int) -> bool:
        """Checks if the current row triggers a buy signal."""
        return not pd.isna(row['buy']) and position == 0

    def _is_sell_signal(self, row: pd.Series, position: int) -> bool:
        """Checks if the current row triggers a sell signal."""
        return not pd.isna(row['sell']) and position == 1

    def _enter_position(self, row: pd.Series, index) -> tuple:
        """Records the entry for a position on a buy signal."""
        entry_price = row['buy']
        self.positions.append(('buy', row['buy'], index))
        return 1, entry_price

    def _exit_position(self, entry_price: float, row: pd.Series, index) -> None:
        """Records the exit of a position on a sell signal."""
        sell_price = row['sell']
        profit = sell_price - entry_price
        self.current_capital += profit
        self.trades.append((entry_price, sell_price, profit, index))
        self.positions.append(('sell', row['sell'], index))

    def _update_portfolio_value(self, index) -> None:
        """Updates the portfolio value based on current capital."""
        self.portfolio_values.at[index] = self.current_capital

    def calculate_metrics(self) -> pd.Series:
        """Calculates backtest metrics like Sharpe Ratio, Annual Return, and Max Drawdown."""
        returns = self.portfolio_values.pct_change().dropna()
        sharpe_ratio = self._calculate_sharpe_ratio(returns)
        annual_return = self._calculate_annual_return()
        max_drawdown = self._calculate_max_drawdown()

        # Compile results
        results = {
            'Initial Capital': self.initial_capital,
            'Final Capital': self.current_capital,
            'Total Trades': len(self.trades),
            'Winning Trades': self._count_winning_trades(),
            'Losing Trades': self._count_losing_trades(),
            'Total Profit': self.current_capital - self.initial_capital,
            'Sharpe Ratio': sharpe_ratio,
            'Annual Return (%)': annual_return,
            'Max Drawdown (%)': max_drawdown
        }

        return pd.Series(results)

    def _calculate_sharpe_ratio(self, returns: pd.Series) -> float:
        """Calculates the Sharpe Ratio of the backtest."""
        return (returns.mean() / returns.std()) * np.sqrt(252) if not returns.empty else 0

    def _calculate_annual_return(self) -> float:
        """Calculates the annual return as a percentage."""
        return (self.portfolio_values.iloc[-1] / self.initial_capital - 1) * 100

    def _calculate_max_drawdown(self) -> float:
        """Calculates the maximum drawdown as a percentage."""
        drawdown = self.portfolio_values.expanding().max() - self.portfolio_values
        return (drawdown.max() / self.portfolio_values.expanding().max()).iloc[-1] * 100

    def _count_winning_trades(self) -> int:
        """Counts the number of winning trades."""
        return len([trade for trade in self.trades if trade[2] > 0])

    def _count_losing_trades(self) -> int:
        """Counts the number of losing trades."""
        return len([trade for trade in self.trades if trade[2] < 0])

    def get_portfolio_values(self) -> pd.Series:
        """Returns the portfolio values over time."""
        return self.portfolio_values
