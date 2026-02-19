# RSI Extreme Engine

Scans top 100 Binance Futures USDT pairs for extreme RSI signals.

Triggers alerts when:
- RSI >= 88 (overbought)
- RSI <= 12 (oversold)

Logs:
- Entry price
- 15-minute exit price
- Percent move

## Setup

1. Add API keys to config.py (or use environment variables)
2. Install requirements:
   pip install -r requirements.txt
3. Run:
   python main.py
