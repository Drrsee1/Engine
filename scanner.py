import pandas as pd
from binance.client import Client
from ta.momentum import RSIIndicator
from logger_config import get_logger
import time

logger = get_logger()

# Use Binance public API (no authentication required)
client = Client()

# Cache for API calls
_cache = {
    'top_symbols': {'data': None, 'timestamp': 0},
    'rsi': {}
}
CACHE_EXPIRY = 60  # Cache expires after 60 seconds

# RSI Parameters
RSI_PERIOD = 14
TOP_COINS_LIMIT = 100
SLEEP_SECONDS = 300
TIMEFRAMES = ["5m", "15m"]
OVERBOUGHT_LEVEL = 88
OVERSOLD_LEVEL = 12
COOLDOWN_MIN = 40
COOLDOWN_MAX = 60

def get_top_symbols():
    """Get top 100 USDT trading pairs by volume (with caching)"""
    try:
        current_time = time.time()
        
        # Return cached data if still valid
        if _cache['top_symbols']['data'] and (current_time - _cache['top_symbols']['timestamp']) < CACHE_EXPIRY:
            logger.debug("Using cached top symbols")
            return _cache['top_symbols']['data']
        
        logger.debug("Fetching top symbols from Binance...")
        tickers = client.futures_ticker()
        usdt_pairs = [t for t in tickers if t["symbol"].endswith("USDT")]
        sorted_pairs = sorted(usdt_pairs, key=lambda x: float(x["quoteVolume"]), reverse=True)
        
        result = [p["symbol"] for p in sorted_pairs[:TOP_COINS_LIMIT]]
        
        # Update cache
        _cache['top_symbols']['data'] = result
        _cache['top_symbols']['timestamp'] = current_time
        
        return result
        
    except Exception as e:
        logger.error(f"Error fetching top symbols: {e}")
        return []

def get_rsi(symbol, interval, retries=2):
    """Get RSI for symbol and timeframe with caching and retry logic"""
    try:
        cache_key = f"{symbol}_{interval}"
        current_time = time.time()
        
        # Return cached data if still valid
        if cache_key in _cache['rsi']:
            cached = _cache['rsi'][cache_key]
            if (current_time - cached['timestamp']) < CACHE_EXPIRY:
                logger.debug(f"Using cached RSI for {symbol} {interval}")
                return cached['value']
        
        # Try to fetch with retries
        for attempt in range(retries):
            try:
                logger.debug(f"Fetching RSI for {symbol} {interval} (attempt {attempt + 1})")
                klines = client.futures_klines(symbol=symbol, interval=interval, limit=100)
                
                if not klines or len(klines) == 0:
                    logger.debug(f"No klines for {symbol} {interval}")
                    continue

                df = pd.DataFrame(klines, columns=[
                    "time","open","high","low","close","volume",
                    "_","_","_","_","_","_"
                ])

                df["close"] = df["close"].astype(float)
                rsi = RSIIndicator(df["close"], RSI_PERIOD).rsi().iloc[-1]

                # Validate RSI value
                if isinstance(rsi, (int, float)) and 0 <= rsi <= 100:
                    # Update cache
                    _cache['rsi'][cache_key] = {'value': rsi, 'timestamp': current_time}
                    return rsi
                else:
                    logger.debug(f"Invalid RSI value for {symbol}: {rsi}")
                    continue
                    
            except Exception as e:
                if attempt < retries - 1:
                    time.sleep(0.5)
                    continue
                logger.error(f"Error fetching RSI for {symbol} {interval}: {e}")
                return None
        
        return None
        
    except Exception as e:
        logger.error(f"Unexpected error in get_rsi for {symbol}: {e}")
        return None

def analyze_symbol(symbol):
    """Analyze symbol RSI levels across multiple timeframes"""
    try:
        rsis = []

        for tf in TIMEFRAMES:
            rsi = get_rsi(symbol, tf)
            if rsi is not None:
                rsis.append(rsi)

        if not rsis:
            return False, False, 0

        overbought = all(r >= OVERBOUGHT_LEVEL for r in rsis)
        oversold = all(r <= OVERSOLD_LEVEL for r in rsis)

        return overbought, oversold, rsis
        
    except Exception as e:
        logger.error(f"Error analyzing {symbol}: {e}")
        return False, False, []
