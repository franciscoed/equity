import yfinance as yf
import streamlit as st
import datetime
import talib
import pandas as pd
import requests

yf.pdr_override()


def get_symbol(symbol):
    url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(
        symbol
    )
    result = requests.get(url).json()
    for x in result["ResultSet"]["Result"]:
        if x["symbol"] == symbol:
            return x["name"]


st.sidebar.header("User Input Parameters")

today = datetime.date.today()
date_from = date_from = (today - datetime.timedelta(days=366)).strftime("%Y-%m-%d")

symbol = st.sidebar.selectbox("Ticker", ["PETR4.SA", "VALE3.SA"])
company_name = get_symbol(symbol.upper())

st.write(company_name)


start = pd.to_datetime(date_from)
end = pd.to_datetime(today)

# Read data
data = yf.download(symbol, start, end)

# Adjusted Close Price
st.header(f"Adjusted Close Price")
st.line_chart(data["Adj Close"])

indicator_list = st.sidebar.multiselect(
    "Indicators", ["SMA/EMA", "Bollinger Bands", "MACD", "RSI"]
)


if "SMA/EMA" in indicator_list:
    ma_periods = st.sidebar.text_input("SMA/EMA Periods", value=13)
    try:
        ma_periods_int = int(ma_periods)
    except:
        ma_periods_int = 13
    # ## SMA and EMA
    # Simple Moving Average
    data["SMA"] = talib.SMA(data["Adj Close"], timeperiod=ma_periods_int)

    # Exponential Moving Average
    data["EMA"] = talib.EMA(data["Adj Close"], timeperiod=ma_periods_int)

    # Plot
    st.header(f"SMA/EMA - Periods: {ma_periods_int}")
    st.line_chart(data[["Adj Close", "SMA", "EMA"]])

if "Bollinger Bands" in indicator_list:
    # Bollinger Bands
    data["upper_band"], data["middle_band"], data["lower_band"] = talib.BBANDS(
        data["Adj Close"], timeperiod=20
    )

    # Plot
    st.header(f"Bollinger Bands")
    st.line_chart(data[["Adj Close", "upper_band", "middle_band", "lower_band"]])


if "MACD" in indicator_list:
    # ## MACD (Moving Average Convergence Divergence)
    # MACD
    data["macd"], data["macdsignal"], data["macdhist"] = talib.MACD(
        data["Adj Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )

    # Plot
    st.header(f"Moving Average Convergence Divergence")
    st.line_chart(data[["macd", "macdsignal"]])

if "RSI" in indicator_list:
    # ## RSI (Relative Strength Index)
    # RSI
    data["RSI"] = talib.RSI(data["Adj Close"], timeperiod=14)

    # Plot
    st.header(f"Relative Strength Index")
    st.line_chart(data["RSI"])

# ## OBV (On Balance Volume)
# OBV
data["OBV"] = talib.OBV(data["Adj Close"], data["Volume"]) / 10 ** 6
# Plot
st.header(f"On Balance Volume")
st.bar_chart(data["OBV"])

if st.checkbox("View raw data"):
    if st.checkbox("Reverse", value=True):
        "Raw Data", data[::-1]
    else:
        "Raw Data", data
