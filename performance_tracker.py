import csv
from binance.client import Client
from config import *

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)
FILE_NAME = "signals_log.csv"

def get_current_price(symbol):
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

def update_last_signal(symbol):
    # Read all rows
    with open(FILE_NAME, "r") as file:
        rows = list(csv.reader(file))

    # Find the last entry for this symbol without exit price
    for i in range(len(rows)-1, 0, -1):
        if rows[i][1] == symbol and rows[i][5] == "":
            entry_price = float(rows[i][4])
            exit_price = get_current_price(symbol)

            percent_move = ((exit_price - entry_price) / entry_price) * 100

            rows[i][5] = round(exit_price, 4)
            rows[i][6] = round(percent_move, 4)
            break

    # Write back updated CSV
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
