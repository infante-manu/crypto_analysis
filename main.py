"""Main script to execute the crypto analysis project."""

from crypto_analysis.trading_engine import TradingEngine, Config
import argparse

if __name__ == '__main__':
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run the crypto trading simulator.")
    parser.add_argument('--pair', type=str, default='ETHUSD', help='Trading pair to analyze (default: ETHUSD)')
    parser.add_argument('--interval', type=int, default=1440, help='Interval in minutes (default: 1440)')
    parser.add_argument('--oversold', type=int, default=30, help='Oversold RSI threshold (default: 30)')
    parser.add_argument('--overbought', type=int, default=70, help='Overbought RSI threshold (default: 70)')
    parser.add_argument('--initial_capital', type=float, default=10000, help='Initial capital for backtesting (default: 10000)')
    parser.add_argument('--since', type=int, default=None, help='Historical data start timestamp (optional)')

    # Parse arguments from CLI
    args = parser.parse_args()

    # Create Config object from CLI arguments
    config = Config(
        pair=args.pair,
        interval=args.interval,
        oversold=args.oversold,
        overbought=args.overbought,
        initial_capital=args.initial_capital,
        since=args.since
    )

    # Initialize the TradingEngine with the configuration
    engine = TradingEngine(config=config)

    # Run the trading strategy
    engine.run()

    # Retrieve and display processed data
    processed_data = engine.data_processor.get_processed_data()
    print("Processed Data:")
    print(processed_data)

    # Retrieve and display signals
    print("Generated Signals:")
    print(engine.get_signals().dropna(subset=['buy', 'sell'], how='all'))

    # Retrieve and display backtest results
    print("Backtest Results:")
    print(engine.get_backtest_results())
