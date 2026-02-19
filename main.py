import time
from scanner import get_top_symbols, analyze_symbol
from telegram import send_message
from signal_logger import log_signal, update_signal
from performance_tracker import update_last_signal
from binance.client import Client
from logger_config import get_logger
from health_check import start_health_check_server
import threading

logger = get_logger()

# Use Binance public API (no authentication required)
client = Client()

def get_current_price(symbol, retries=2):
    """Get current price for symbol with retry logic"""
    for attempt in range(retries):
        try:
            ticker = client.futures_symbol_ticker(symbol=symbol)
            if ticker and isinstance(ticker, dict) and 'price' in ticker:
                price = float(ticker['price'])
                if price > 0:
                    return price
            else:
                logger.debug(f"Invalid ticker response for {symbol}: {ticker}")
        except Exception as e:
            logger.debug(f"Attempt {attempt + 1} failed for {symbol}: {e}")
            if attempt < retries - 1:
                time.sleep(0.5)  # Small delay before retry
                continue
        
    logger.warning(f"Could not get price for {symbol} after {retries} attempts")
    return None

def run():
    """Main bot loop"""
    logger.info("=" * 50)
    logger.info("RSI Extreme Engine started (Public API)")
    logger.info("=" * 50)
    
    alerted = {}
    alert_cooldown = {}  # timestamp-based cooldown
    
    # Start health check server in background
    start_health_check_server()
    
    while True:
        try:
            symbols = get_top_symbols()
            
            if not symbols:
                logger.warning("No symbols retrieved, retrying...")
                time.sleep(300)
                continue
            
            logger.debug(f"Analyzing {len(symbols)} symbols...")

            for symbol in symbols:
                try:
                    # Skip if we've already alerted on this symbol recently
                    current_time = time.time()
                    if symbol in alert_cooldown:
                        cooldown_elapsed = current_time - alert_cooldown[symbol]
                        if cooldown_elapsed < (40 * 60):  # 40 minute cooldown
                            continue
                    
                    # Get current price first to validate the symbol
                    current_price = get_current_price(symbol)
                    if current_price is None:
                        logger.debug(f"Skipping {symbol} - price unavailable")
                        continue
                    
                    # Now analyze RSI
                    overbought, oversold, rsi_values = analyze_symbol(symbol)
                    
                    if not rsi_values:
                        continue

                    # OVERBOUGHT signal
                    if overbought and symbol not in alerted:
                        logger.warning(f"🔴 OVERBOUGHT detected: {symbol} @ ${current_price:.4f}")
                        send_message(symbol, "overbought", rsi_values, current_price)
                        log_signal(symbol, "overbought", rsi_values, current_price)
                        alerted[symbol] = True
                        alert_cooldown[symbol] = current_time

                        time.sleep(900)  # wait 15 minutes before next
                        update_signal(symbol, current_price)

                    # OVERSOLD signal
                    elif oversold and symbol not in alerted:
                        logger.warning(f"🟢 OVERSOLD detected: {symbol} @ ${current_price:.4f}")
                        send_message(symbol, "oversold", rsi_values, current_price)
                        log_signal(symbol, "oversold", rsi_values, current_price)
                        alerted[symbol] = True
                        alert_cooldown[symbol] = current_time

                        time.sleep(900)  # wait 15 minutes before next
                        update_signal(symbol, current_price)

                    # Clear alert when RSI enters neutral zone
                    if 40 <= rsi_values[-1] <= 60 and symbol in alerted:
                        logger.debug(f"Cooldown reset for {symbol}")
                        del alerted[symbol]

                except Exception as e:
                    logger.error(f"Error processing {symbol}: {e}")
                    continue

            logger.debug(f"Scan complete. Sleeping for 300s...")
            time.sleep(300)

        except KeyboardInterrupt:
            logger.warning("Bot stopped by user")
            break
        except Exception as e:
            logger.error(f"Critical error in main loop: {e}")
            logger.error("Attempting to continue...")
            time.sleep(300)

if __name__ == "__main__":
    run()
