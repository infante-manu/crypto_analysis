from datetime import datetime
import streamlit as st
import pandas as pd

def parse_datetime_to_timestamp(date, time):
    if date is None:
        date = datetime.today().date()
    if time is None:
        time = datetime.now().time()
    datetime_combined = datetime.combine(date, time)
    return int(datetime_combined.timestamp())


def render_backtest_results(results: pd.Series):
    """
    Renders backtest results in a Streamlit app.

    Parameters:
    results (dict): A dictionary containing the backtest results.
    """
    st.title("Backtest Results")

    # Display the results
    st.subheader("Summary")
    st.dataframe(
        results.to_frame(name = "Value"),
        width=800,
        use_container_width = True
        )
