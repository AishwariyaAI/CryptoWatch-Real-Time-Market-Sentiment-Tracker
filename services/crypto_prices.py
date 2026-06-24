import yfinance as yf

def get_crypto_prices():

    btc = yf.Ticker("BTC-USD")
    eth = yf.Ticker("ETH-USD")

    btc_price = btc.history(period="1d")["Close"].iloc[-1]
    eth_price = eth.history(period="1d")["Close"].iloc[-1]

    return round(btc_price, 2), round(eth_price, 2)