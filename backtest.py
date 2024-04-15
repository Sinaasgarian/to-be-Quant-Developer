import vectorbt as vbt
import pandas as pd

btc_price =  vbt.YFData.download('BTC-USD')

print(btc_price.get())

closing_price = btc_price.get()


rsi = vbt.RSI.run(closing_price)

entries = rsi.rsi_below(30)
exits = rsi.rsi_above(70)

print(entries)
print(exits)


portfolio = vbt.Portfolio.from_signals(closing_price, entries, exits, init_cash=1000)
portfolio.plot().show()