import streamlit as st
from crypto_analysis.trading_engine import TradingEngine
import pandas as pd

def main():
    st.title("Cryptocurrency Trading Strategy Simulator")
    
    # User inputs
    pair = st.selectbox("Select the cryptocurrency pair", options=["BTCUSD", "ETHUSD", "LTCUSD"])
    
    start_date = st.date_input("Start date", value=pd.to_datetime("2021-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2021-12-31"))

    interval = st.number_input("Interval (in minutes)", min_value=1, value=60)
    initial_capital = st.number_input("Initial Capital", min_value=100, value=10000)

    oversold = st.number_input("Oversold Level (default 30)", min_value=0, max_value=100, value=30)
    overbought = st.number_input("Overbought Level (default 70)", min_value=0, max_value=100, value=70)

    if st.button("Run Simulation"):
        # Create an instance of TradingEngine with user inputs
        engine = TradingEngine(
            pair=pair, 
            initial_capital=initial_capital
            )
        engine.data_processor = CryptoDataProcessor(pair=pair, interval=interval)
        engine.signal_generator = SignalGenerator(data=engine.data_processor.get_processed_data(), 
                                                  oversold=oversold, 
                                                  overbought=overbought)
        
        # Process data and generate signals
        engine.process_data()
        engine.signals = engine.signal_generator.generate_signals()
        
        # Run backtest
        engine.backtester = Backtester(data=engine.signals, initial_capital=initial_capital)
        engine.backtester.backtest()
        
        # Show results
        st.subheader("Backtest Results")
        st.write("Final Portfolio Value: ", engine.backtester.current_capital)
        st.line_chart(engine.backtester.portfolio_values)

        # Additional details or plots can be displayed here
        st.subheader("Trading Signals")
        st.write(engine.signals[['buy', 'sell']])

if __name__ == "__main__":
    main()
