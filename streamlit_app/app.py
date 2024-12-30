import streamlit as st
from crypto_analysis.trading_engine import TradingEngine, Config
from crypto_analysis.kraken_api_handler import KrakenAPIHandler
from constants import INTERVAL_MAP

def main():
    """
    Main function to run the Streamlit app for Cryptocurrency Trading Strategy Simulator.
    This function sets up the user interface for the app, allowing users to input parameters 
    for a trading strategy simulation, such as the cryptocurrency pair, initial capital, 
    interval, oversold and overbought levels, date, and time. It also includes a button to 
    run the simulation. The simulation is limited to a 700-period backtest based on the 
    selected interval.
    The function performs the following steps:
    1. Displays the title of the app.
    2. Collects user inputs for the trading strategy parameters.
    3. Creates a configuration object with the user inputs.
    4. Initializes the trading engine with the configuration.
    5. Runs the trading simulation.
    6. Displays the trading signals plot, backtest portfolio value plot, trading signals summary, 
       and backtest results summary.
    """
    st.set_page_config(page_title="Trading Simulator")
    st.title("Cryptocurrency Trading Strategy Simulator")
    
    # User inputs
    kraken_api_handler = KrakenAPIHandler()
    available_pairs = kraken_api_handler.get_asset_pairs()

    pair = st.selectbox(
        "Select the cryptocurrency pair", 
        options=available_pairs,
        placeholder="ETHUSD",
        help="Select the cryptocurrency pair to simulate trading strategy."
        )
    
    initial_capital = st.number_input(
        "Initial Capital", 
        min_value=100, 
        value=100000,
        format="%d",
        help="Enter the initial capital for the trading strategy."
        )

    interval = st.selectbox(
        "Interval", 
        options= INTERVAL_MAP.keys(),
        help="Select the interval for the trading strategy."
        )
    
    oversold = st.number_input(
        "Oversold Level (default 30)", 
        min_value=0, 
        max_value=100, 
        value=30,
        help="Enter the oversold level for the RSI indicator. More info: https://en.wikipedia.org/wiki/Relative_strength_index"
        )
    
    overbought = st.number_input(
        "Overbought Level (default 70)", 
        min_value=0, 
        max_value=100, 
        value=70,
        help="Enter the overbought level for the RSI indicator. More info: https://en.wikipedia.org/wiki/Relative_strength_index"
        )


    if st.button("Run Simulation"):
        # Create an instance of TradingEngine with user inputs

        config = Config(
            pair=pair,
            initial_capital=initial_capital,
            interval=INTERVAL_MAP[interval],
            oversold=oversold,
            overbought=overbought
        )

        engine = TradingEngine(config)

        # Run the simulation
        engine.run()

        # Plotting using the TradingEngine methods
        st.subheader("Trading Signals Plot")
        st.plotly_chart(engine.get_data_plot())

        st.subheader("Backtest Portfolio Value Over Time")
        st.plotly_chart(engine.get_portfolio_plot())

        # Display backtest results summary
        st.subheader("Backtest Results Summary")
        result = engine.get_backtest_results()
        st.dataframe(
            result.to_frame(name = ""),
            width=800,
            use_container_width = True
        )

        # Display trading signals summaryis
        st.subheader("Trading Signals Summary")
        st.dataframe(
            engine.get_signals().dropna(subset=["buy", "sell"], how="all"),
            width=1600,
            use_container_width=True
        )


if __name__ == "__main__":
    main()
