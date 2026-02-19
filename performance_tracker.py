from signal_logger import update_signal
from logger_config import get_logger

logger = get_logger()

def update_last_signal(symbol):
    """Update the last signal with exit price and percent move"""
    try:
        update_signal(symbol, exit_price=None)  # Will be fetched inside update_signal
        logger.info(f"Signal updated for {symbol}")
    except Exception as e:
        logger.error(f"Error updating signal for {symbol}: {e}")
