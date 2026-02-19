import pandas as pd
from binance.client import Client
from ta.momentum import RSIIndicator
from config import *

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def get_top_symbols():
    tickers = client.futures_ticker()
    usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
    sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)
    return [p["symbol"] for p in sorted_pairs[:TOP_COINS_LIMIT]]

def get_rsi(symbol, interval):
    klines = client.futures_klines(symbol=symbol, interval=interval, limit=100)

    df = pd.DataFrame(klines, columns=[
        "time","open","high","low","close","volume",
        "_","_","_","_","_","_"
    ])

    df["close"] = df["close"].astype(float)
    rsi = RSIIndicator(df["close"], RSI_PERIOD).rsi().iloc[-1]

    return rsi

def analyze_symbol(symbol):
    rsis = []

    for tf in TIMEFRAMES:
        rsi = get_rsi(symbol, tf)
        rsis.append(rsi)

    overbought = all(r >= OVERBOUGHT_LEVEL for r in rsis)
    oversold = all(r <= OVERSOLD_LEVEL for r in rsis)

    return overbought, oversold, rsis[-1]
