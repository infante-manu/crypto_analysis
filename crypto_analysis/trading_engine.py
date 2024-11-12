from typing import Optional
import pandas as pd
from crypto_analysis.crypto_data_processor import CryptoDataProcessor
from crypto_analysis.signal_generator import SignalGenerator
from crypto_analysis.crypto_plotter import CryptoPlotter
from crypto_analysis.backtester import Backtester

class Config:
    def __init__(self, pair: str, interval: int = 1440, oversold: int = 30, overbought: int = 70, initial_capital: float = 10000):
        self.pair = pair
        self.interval = interval
        self.oversold = oversold
        self.overbought = overbought
        self.initial_capital = initial_capital

class TradingEngine:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.data_processor = CryptoDataProcessor(
            pair=config.pair,
            interval=config.interval,
            oversold=config.oversold,
            overbought=config.overbought
        )
        self.initial_capital: float = config.initial_capital
        self.signal_generator: Optional[SignalGenerator] = None
        self.processed_data: Optional[pd.DataFrame] = None
        self.signals: Optional[pd.DataFrame] = None
        self.backtester: Optional[Backtester] = None
        self.backtest_results: Optional[pd.DataFrame] = None
        self.portfolio_values: Optional[pd.Series] = None
        self.plotter: Optional[CryptoPlotter] = None

    def process_data(self) -> None:
        """Processes raw data to add technical indicators."""
        self.processed_data = self.data_processor.get_processed_data()
        self.signal_generator = SignalGenerator(self.processed_data)

    def generate_signals(self) -> None:
        """Generates trading signals and prepares data for visualization."""
        self.signals = self.signal_generator.generate_signals()
        self.plotter = CryptoPlotter(self.signals)

    def backtest(self) -> None:
        """Runs the backtest on the generated signals."""
        self.backtester = Backtester(self.signals, initial_capital=self.initial_capital)
        self.backtest_results = self.backtester.run_backtest()
        self.portfolio_values = self.backtester.get_portfolio_values()

    def run(self) -> None:
        """Executes the full trading strategy."""
        self.process_data()
        self.generate_signals()
        self.backtest()

    def get_signals(self) -> pd.DataFrame:
        """Returns generated trading signals."""
        return self.signals

    def get_backtest_results(self) -> pd.DataFrame:
        """Returns backtest performance metrics."""
        return self.backtest_results

    def plot_strategy(self) -> None:
        """Plots the strategy's data visualization."""
        self.plotter.plot_data()

    def plot_portfolio(self) -> None:
        """Plots the portfolio performance over time."""
        self.plotter.plot_portfolio(self.portfolio_values, self.initial_capital)

    def get_data_plot(self):
        """Returns the Plotly data plot object."""
        return self.plotter.get_data_plot()

    def get_portfolio_plot(self):
        """Returns the Plotly portfolio plot object."""
        return self.plotter.get_portfolio_plot(self.portfolio_values, self.initial_capital)


if __name__ == '__main__':
    # Example usage
    engine = TradingEngine(pair='ETHUSD')
    engine.run()
    processed_data = engine.data_processor.get_processed_data()
    print(processed_data)
    print(engine.signals.dropna(subset = ['buy', 'sell'], how = 'all'))