import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import requests
import os

yf.pdr_override()


def download(url, file_name):
    # open in binary mode
    with open(file_name, "wb") as file:
        # get request
        response = requests.get(url)
        # write to file
        file.write(response.content)


download(
    "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz",
    "/tmp/ta-lib-0.4.0-src.tar.gz",
)
os.chdir("/tmp")
os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
os.chdir("/tmp/ta-lib")
os.system("./configure --prefix=/tmp")
os.system("make")
os.system("make install")
os.system(
    'pip3 install --global-option=build_ext --global-option="-L/tmp/lib/" --global-option="-I/tmp/include/" ta-lib'
)
os.chdir("/app/equity")


import talib


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

symbol = st.sidebar.selectbox(
    "Ticker", ["PETR4.SA", "VALE3.SA", "ABEV3.SA", "AZUL4.SA"]
)
company_name = get_symbol(symbol.upper())

st.write(company_name)


start = pd.to_datetime(date_from)
end = pd.to_datetime(today)

# Read data
data = yf.download(symbol, start, end)


# Adjusted Close Price
st.header(f"Adjusted Close Price")
st.line_chart(data["Adj Close"])
df_table = data.copy()
del df_table["Open"]
del df_table["High"]
del df_table["Low"]
del df_table["Close"]
del df_table["Volume"]


data["SMA"] = talib.SMA(data["Adj Close"], timeperiod=ma_periods_int)
df_table["SMA"] = data["SMA"]

# Exponential Moving Average
data["EMA"] = talib.EMA(data["Adj Close"], timeperiod=ma_periods_int)
df_table["EMA"] = data["EMA"]

# Plot
st.header(f"SMA/EMA - Periods: {ma_periods_int}")
st.line_chart(data[["Adj Close", "SMA", "EMA"]])

if st.checkbox("View raw data"):
    if st.checkbox("Reverse", value=True):
        "Raw Data", data[::-1]
    else:
        "Raw Data", data
