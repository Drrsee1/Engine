import csv
import os
import datetime

FILE_NAME = "signals_log.csv"

def log_signal(symbol, signal_type, rsi_value, entry_price):
    file_exists = os.path.isfile(FILE_NAME)

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)

        # If file does not exist, write header first
        if not file_exists:
            writer.writerow([
                "timestamp",
                "symbol",
                "signal_type",
                "rsi",
                "entry_price",
                "exit_price_15m",
                "percent_move_15m"
            ])

        # Write the signal
        writer.writerow([
            datetime.datetime.utcnow(),
            symbol,
            signal_type,
            round(rsi_value, 2),
            entry_price,
            "",
            ""
        ])
