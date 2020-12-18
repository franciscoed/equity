import yfinance as yf
import streamlit as st
import datetime
import pandas as pd
import requests
import os
import sys



# check if the library folder already exists, to avoid building everytime you load the pahe
if not os.path.isdir("/tmp/ta-lib"):

    # Download ta-lib to disk
    with open("/tmp/ta-lib-0.4.0-src.tar.gz", "wb") as file:
        response = requests.get(
            "http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz"
        )
        file.write(response.content)
    # get our current dir, to configure it back again. Just house keeping
    default_cwd = os.getcwd()
    os.chdir("/tmp")
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    os.system("make install")
    os.system(
        'pip3 install --global-option=build_ext --global-option="-L/home/appuser/lib/" --global-option="-I/home/appuser/include/" ta-lib'
    )
    os.chdir(default_cwd)
    print(os.getcwd())
    sys.stdout.flush()


from ctypes import *

lib = CDLL("/home/appuser/lib/libta_lib.so.0")

import talib


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

ma_periods_int = 13
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
