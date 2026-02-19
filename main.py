import time
from scanner import get_top_symbols, analyze_symbol
from telegram import send_message
from signal_logger import log_signal
from performance_tracker import update_last_signal
from binance.client import Client
from config import *

client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

def run():
    alerted = {}

    while True:
        symbols = get_top_symbols()

        for symbol in symbols:
            try:
                overbought, oversold, rsi = analyze_symbol(symbol)
                current_price = float(client.futures_symbol_ticker(symbol=symbol)["price"])

                if overbought and symbol not in alerted:
                    send_message(
                        f"EXTREME OVERBOUGHT\n\n{symbol}\nRSI: {rsi:.2f}\nEntry: {current_price}"
                    )
                    log_signal(symbol, "overbought", rsi, current_price)
                    alerted[symbol] = True

                    time.sleep(900)  # wait 15 minutes
                    update_last_signal(symbol)

                elif oversold and symbol not in alerted:
                    send_message(
                        f"EXTREME OVERSOLD\n\n{symbol}\nRSI: {rsi:.2f}\nEntry: {current_price}"
                    )
                    log_signal(symbol, "oversold", rsi, current_price)
                    alerted[symbol] = True

                    time.sleep(900)  # wait 15 minutes
                    update_last_signal(symbol)

                # Reset cooldown
                if COOLDOWN_MIN <= rsi <= COOLDOWN_MAX and symbol in alerted:
                    del alerted[symbol]

            except Exception:
                continue

        time.sleep(SLEEP_SECONDS)

if __name__ == "__main__":
    run()
