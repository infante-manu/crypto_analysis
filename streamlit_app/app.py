import streamlit as st
from crypto_analysis.trading_engine import TradingEngine
from crypto_analysis.kraken_api_handler import KrakenAPIHandler
import pandas as pd

def main():
    st.title("Cryptocurrency Trading Strategy Simulator")
    
    # User inputs
    kraken_api_handler = KrakenAPIHandler()
    available_pairs = kraken_api_handler.get_available_pairs()
    pair = st.selectbox(
        "Select the cryptocurrency pair", 
        options=available_pairs,
        placeholder="ETHUSD"
        )
    
    start_date = st.date_input("Start date", value=pd.to_datetime("2021-01-01"))
    end_date = st.date_input("End date", value=pd.to_datetime("2021-12-31"))

    interval = st.number_input("Interval (in minutes)", min_value=1, value=60)
    initial_capital = st.number_input("Initial Capital", min_value=100, value=100000)

    oversold = st.number_input("Oversold Level (default 30)", min_value=0, max_value=100, value=30)
    overbought = st.number_input("Overbought Level (default 70)", min_value=0, max_value=100, value=70)

    if st.button("Run Simulation"):
        # Create an instance of TradingEngine with user inputs
        engine = TradingEngine(
            pair=pair, 
            initial_capital=initial_capital,
            # start_date = start_date,
            # end_date = end_date,
            # interval = interval,
            # oversold = oversold,
            # overbought = overbought
            )
        
        # Run the simulation
        engine.run()

        # Plotting using the TradingEngine methods
        st.subheader("Trading Signals Plot")
        st.plotly_chart(engine.get_data_plot())

        st.subheader("Backtest Portfolio Value Over Time")
        st.plotly_chart(engine.get_portfolio_plot())

        # Display trading signals summary
        st.subheader("Trading Signals Summary")
        st.dataframe(engine.get_signals())

        # Display backtest results summary
        st.subheader("Backtest Results Summary")
        st.dataframe(engine.get_backtest_results())

if __name__ == "__main__":
    main()
