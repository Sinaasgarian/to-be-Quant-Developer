from IPython.display import display, HTML

import vectorbt as vbt
import yfinance as yf
import talib  # Add this line

data = yf.download("BTC-USD", start="2020-01-01", end="2022-06-01")

hammer = talib.CDLHAMMER(data.open, data.high, data.low, data.Close)

print(hammer[hammer == 100].to_frame())  # Add .to_frame()
display(data)