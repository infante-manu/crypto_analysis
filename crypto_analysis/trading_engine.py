from crypto_analysis.crypto_data_processor import CryptoDataProcessor
from crypto_analysis.signal_generator import SignalGenerator
from crypto_analysis.crypto_plotter import CryptoPlotter
from crypto_analysis.backtester import Backtester

class TradingEngine:
    def __init__(self, pair: str, initial_capital : float = 10000) -> None:
        self.pair = pair
        self.data_processor = CryptoDataProcessor(pair = pair, interval = 1)
        self.initial_capital = initial_capital
        self.signal_generator = None
        self.processed_data = None
        self.signals = None
        self.backtester = None
        self.backtest_results = None
        self.portfolio_values = None
        self.plotter = None

    def process_data(self) -> None:
        self.processed_data = self.data_processor.get_processed_data()
        self.signal_generator = SignalGenerator(self.processed_data)

    def generate_signals(self) -> None:
        self.signals = self.signal_generator.generate_signals()
        self.plotter = CryptoPlotter(self.signals)

    def backtest(self) -> None:
        self.backtester = Backtester(self.signals, initial_capital = self.initial_capital)
        self.backtest_results = self.backtester.run_backtest()
        self.portfolio_values = self.backtester.get_portfolio_values()

    def run(self) -> None:
        self.process_data()
        self.generate_signals()
        self.backtest()

    def get_signals(self):
        return self.signals
    
    def get_backtest_results(self):
        return self.backtest_results
    
    def plot_strategy(self):
        self.plotter.plot_data()
        return 
    
    def plot_portafolio(self):
        self.plotter.plot_portfolio(self.portfolio_values, self.initial_capital)
        return 
    
    def plot_strategy(self):
        self.plotter.plot_data()
        return 
    
    def plot_portafolio(self):
        self.plotter.plot_portfolio(self.portfolio_values, self.initial_capital)
        return 
    
    def get_data_plot(self):
        return self.plotter.get_data_plot()
         
    def get_portfolio_plot(self):
        return self.plotter.get_portfolio_plot(self.portfolio_values, self.initial_capital)

if __name__ == '__main__':
    # Example usage
    engine = TradingEngine(pair='ETHUSD')
    engine.run()
    processed_data = engine.data_processor.get_processed_data()
    print(processed_data)
    print(engine.signals.dropna(subset = ['buy', 'sell'], how = 'all'))