from dotenv import load_dotenv
import sys
import os
load_dotenv()
ROOTPATH = os.getenv("ROOTPATH")
sys.path.insert(0, ROOTPATH)  # Insert at the beginning of the list
import pytest
import pandas as pd
import numpy as np
from crypto_analysis.trading_engine import TradingEngine, Config
from crypto_analysis.crypto_data_processor import CryptoDataProcessor
from crypto_analysis.signal_generator import SignalGenerator
from crypto_analysis.backtester import Backtester
from crypto_analysis.crypto_plotter import CryptoPlotter
from crypto_analysis.kraken_api_handler import KrakenAPIHandler

@pytest.fixture
def sample_data():
    """Fixture for providing sample data for testing."""
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    data = pd.DataFrame({
        "time": dates,
        "close": np.random.uniform(100, 200, size=100),
        "upper_band": np.random.uniform(150, 250, size=100),
        "lower_band": np.random.uniform(50, 150, size=100),
        "rsi": np.random.uniform(10, 90, size=100),
        "over_sold": [30] * 100,
        "over_bought": [70] * 100
    })
    data.set_index("time", inplace=True)
    return data

# Test Config
def test_config_initialization():
    config = Config(pair="ETHUSD", interval=1440, oversold=30, overbought=70)
    assert config.pair == "ETHUSD"
    assert config.interval == 1440
    assert config.oversold == 30
    assert config.overbought == 70

# Test CryptoDataProcessor
def test_crypto_data_processor(mocker, sample_data):
    mocker.patch.object(KrakenAPIHandler, "fetch_ohlc_data", return_value=sample_data)
    processor = CryptoDataProcessor(pair="ETHUSD")
    processed_data = processor.get_processed_data()
    assert not processed_data.empty
    assert "upper_band" in processed_data.columns

# Test SignalGenerator
def test_signal_generator(sample_data):
    generator = SignalGenerator(sample_data)
    signals = generator.generate_signals()
    assert "buy" in signals.columns
    assert "sell" in signals.columns

# Test Backtester
def test_backtester(sample_data):
    sample_data["buy"] = np.where(sample_data["rsi"] < 30, sample_data["close"], np.nan)
    sample_data["sell"] = np.where(sample_data["rsi"] > 70, sample_data["close"], np.nan)
    backtester = Backtester(data=sample_data, initial_capital=10000)
    results = backtester.run_backtest()
    assert isinstance(results, pd.Series)

# Test CryptoPlotter
def test_crypto_plotter(sample_data):
    plotter = CryptoPlotter(sample_data)
    assert plotter.data.equals(sample_data)
    # Plotting checks are typically visual; here we ensure no errors occur during calls
    plotter.get_data_plot()

# Test TradingEngine
def test_trading_engine(mocker, sample_data):
    mocker.patch.object(KrakenAPIHandler, "fetch_ohlc_data", return_value=sample_data)
    config = Config(pair="ETHUSD", interval=1440, oversold=30, overbought=70)
    engine = TradingEngine(config)
    engine.run()

    assert engine.processed_data is not None
    assert engine.signals is not None
    assert engine.backtest_results is not None
