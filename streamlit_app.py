import streamlit as st
import yfinace as yf
import requests
import os
import sys
import subprocess

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
    # untar
    os.system("tar -zxvf ta-lib-0.4.0-src.tar.gz")
    os.chdir("/tmp/ta-lib")
    os.system("ls -la /app/equity/")
    # build
    os.system("./configure --prefix=/home/appuser")
    os.system("make")
    # install
    os.system("make install")
    # back to the cwd
    os.chdir(default_cwd)
    sys.stdout.flush()

# add the library to our current environment
from ctypes import *

lib = CDLL("/home/appuser/lib/libta_lib.so.0.0.0")
# import library
try:
    import talib
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--global-option=build_ext", "--global-option=-L/home/appuser/lib/", "--global-option=-I/home/appuser/include/", "ta-lib"])
finally:
    import talib

st.write("Hello")

yf.pdr_override()


# # def get_symbol(symbol):
# #     url = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query={}&region=1&lang=en".format(
# #         symbol
# #     )
# #     result = requests.get(url).json()
# #     for x in result["ResultSet"]["Result"]:
# #         if x["symbol"] == symbol:
# #             return x["name"]


st.sidebar.header("User Input Parameters")

today = datetime.date.today()
date_from = date_from = (today - datetime.timedelta(days=366)).strftime("%Y-%m-%d")

symbol = st.sidebar.selectbox(
    "Ticker", ["PETR4.SA", "VALE3.SA", "ABEV3.SA", "AZUL4.SA"]
)
# company_name = get_symbol(symbol.upper())

st.write(symbol.upper())


start = pd.to_datetime(date_from)
end = pd.to_datetime(today)

# Read data
data = yf.download(symbol, start, end)

st.write("Yahoo .... ok")


# # Adjusted Close Price
# st.header(f"Adjusted Close Price")
# st.line_chart(data["Adj Close"])
# df_table = data.copy()
# del df_table["Open"]
# del df_table["High"]
# del df_table["Low"]
# del df_table["Close"]
# del df_table["Volume"]


# # Candlesticks - Plotly
# data["Date"] = data.index

# fig = go.Figure(
#     data=[
#         go.Candlestick(
#             x=data["Date"],
#             open=data["Open"],
#             high=data["High"],
#             low=data["Low"],
#             close=data["Close"],
#             name=symbol,
#         )
#     ]
# )

# fig.update_layout(
#     title=symbol + " Daily Chart",
#     xaxis_title="Date",
#     yaxis_title="Price ($)",
#     # font=dict(family="Courier New, monospace", size=12, color="black"),
# )

# st.plotly_chart(fig, use_container_width=True)


# # Candlesticks - ALtair
# base = alt.Chart(data).encode(
#     alt.X("Date:T", axis=alt.Axis(labelAngle=-45)),
#     color=alt.condition(
#         "datum.Open <= datum.Close", alt.value("#06982d"), alt.value("#ae1325")
#     ),
# )

# chart = alt.layer(
#     base.mark_rule().encode(
#         alt.Y("Low:Q", title="Price", scale=alt.Scale(zero=False)), alt.Y2("High:Q")
#     ),
#     base.mark_bar().encode(alt.Y("Open:Q"), alt.Y2("Close:Q")),
# ).interactive()
# st.altair_chart(chart, use_container_width=True)
# # open_close_color = alt.condition(
# #     "datum.Open <= datum.Close", alt.value("#06982d"), alt.value("#ae1325")
# # )
# # base = alt.Chart(data).encode(x="Date")
# # rule = base.mark_rule().encode(
# #     y=alt.Y("Low", scale=alt.Scale(zero=False), axis=alt.Axis(title="Price")),
# #     y2=alt.Y2("High"),
# #     color=open_close_color,
# # )
# # bar = base.mark_bar().encode(y="Open", y2="Close", color=open_close_color)
# # st.altair_chart(rule + bar, use_container_width=True)


# # # Candlesticks Bokeh
# # from bokeh.sampledata.stocks import MSFT
# # from math import pi

# # df = pd.DataFrame(MSFT)[:50]
# # df["date"] = pd.to_datetime(df["date"])

# # inc = df.close > df.open
# # dec = df.open > df.close
# # w = 12 * 60 * 60 * 1000  # half day in ms

# # TOOLS = "pan,wheel_zoom,box_zoom,reset"

# # p = figure(
# #     x_axis_type="datetime", tools=TOOLS, plot_width=1000, title="MSFT Candlestick"
# # )
# # p.xaxis.major_label_orientation = pi / 4
# # p.grid.grid_line_alpha = 0.3

# # p.segment(df.date, df.high, df.date, df.low, color="black")
# # p.vbar(
# #     df.date[inc],
# #     w,
# #     df.open[inc],
# #     df.close[inc],
# #     fill_color="#06982d",
# #     line_color="#06982d",
# # )
# # p.vbar(
# #     df.date[dec],
# #     w,
# #     df.open[dec],
# #     df.close[dec],
# #     fill_color="#ae1325",
# #     line_color="#ae1325",
# # )

# # st.bokeh_chart(p, use_container_width=True)

# ma_periods_int = 13
# data["SMA"] = talib.SMA(data["Adj Close"], timeperiod=ma_periods_int)
# df_table["SMA"] = data["SMA"]

# # Exponential Moving Average
# data["EMA"] = talib.EMA(data["Adj Close"], timeperiod=ma_periods_int)
# df_table["EMA"] = data["EMA"]

# # Plot
# st.header(f"SMA/EMA - Periods: {ma_periods_int}")
# st.line_chart(data[["Adj Close", "SMA", "EMA"]])

# if st.checkbox("View raw data"):
#     if st.checkbox("Reverse", value=True):
#         "Raw Data", data[::-1]
#     else:
#         "Raw Data", data
