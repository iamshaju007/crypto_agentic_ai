import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go

def render_dashboard(api_base_url):
    st.subheader("Live Crypto Prices & Predictions")

    # Fetch available cryptocurrencies
    response = requests.get(f"{api_base_url}/crypto/list")
    if response.status_code == 200:
        cryptos = response.json()
    else:
        st.error("Failed to fetch crypto list")
        return

    # User input for crypto and date range
    crypto = st.selectbox("Select Cryptocurrency", cryptos)
    start_date = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
    end_date = st.date_input("End Date", pd.to_datetime("2025-12-31"))

    if start_date >= end_date:
        st.error("Start date must be before end date")
        return

    # Fetch historical data
    params = {"symbol": crypto, "start_date": start_date.strftime("%Y-%m-%d"), "end_date": end_date.strftime("%Y-%m-%d")}
    response = requests.get(f"{api_base_url}/crypto/historical", params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])

        # Closing price chart
        st.subheader(f"{crypto} Closing Prices")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["date"], y=df["close"], mode="lines", name="Closing Price", line=dict(color="royalblue")))
        fig.update_layout(title=f"{crypto} Closing Prices", xaxis_title="Date", yaxis_title="Price (USD)")
        st.plotly_chart(fig)

        # Predictions
        response = requests.get(f"{api_base_url}/predictions/forecast", params={"symbol": crypto})
        if response.status_code == 200:
            pred_data = response.json()
            pred_df = pd.DataFrame(pred_data)
            pred_df["date"] = pd.to_datetime(pred_df["date"])

            st.subheader(f"{crypto} Price Predictions")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df["date"], y=df["close"], mode="lines", name="Historical", line=dict(color="royalblue")))
            fig.add_trace(go.Scatter(x=pred_df["date"], y=pred_df["predicted"], mode="lines", name="Predicted", line=dict(color="darkgreen")))
            fig.update_layout(title=f"{crypto} Price Forecast", xaxis_title="Date", yaxis_title="Price (USD)")
            st.plotly_chart(fig)

        # Staking Recommendations
        response = requests.get(f"{api_base_url}/agents/strategy", params={"symbol": crypto})
        if response.status_code == 200:
            strategy = response.json()
            st.subheader("Staking/Trading Recommendation")
            st.write(strategy["recommendation"])