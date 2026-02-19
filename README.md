# 🤖 RSI Extreme Engine

**Advanced cryptocurrency trading bot that scans 100+ Binance Futures pairs for extreme RSI signals and sends real-time alerts.**

---

## ✨ Features

### 🔔 Real-Time Alerts
- **Telegram** - Live alerts every 5 minutes
- **WhatsApp** - Optional group notifications (PyWhatKit)
- **Email** - Optional email alerts (Gmail)

### 📊 Smart Analysis
- Scans top 100 USDT pairs by volume
- Calculates RSI on 5m + 15m timeframes
- Triggers when **RSI ≥ 88** (overbought) or **RSI ≤ 12** (oversold)
- Logs entry price, exit price, and percent move

### 💾 Professional Features
- **SQLite Database** - Persistent signal logging
- **Logging System** - Debug logs + file storage
- **Health Check API** - Monitor bot status on port 5000
- **Error Handling** - Retry logic + validation
- **Caching** - Optimized API calls (60s cache)

### 🔒 Security
- **Public API only** - No API keys needed ✓
- **Environment variables** - Secrets never committed
- **Read-only operations** - Can't trade/withdraw

---

## 🚀 Quick Start

### Local Development

```bash
# 1. Clone & install
git clone https://github.com/Drrsee1/Engine.git
cd Engine
pip install -r requirements.txt

# 2. Configure
cp .env.example .env
# Edit .env with your Telegram token & Chat ID

# 3. Run
python main.py

# 4. Test alerts
python test_alert.py
```

### Replit Cloud (Recommended)

1. **Import from GitHub:** https://replit.com/github/Drrsee1/Engine
2. **Add Secrets** (🔒 icon):
   - `TELEGRAM_TOKEN` = Your bot token
   - `CHAT_ID` = Your Telegram ID
3. **Run:** `python main.py`
4. **Keep alive:** Enable "Always On" or use UptimeRobot

👉 **[Full Replit Deployment Guide →](REPLIT_DEPLOYMENT.md)**

---

## 📋 Configuration

Create `.env` file:

```
TELEGRAM_TOKEN=your_token_here
CHAT_ID=your_chat_id_here
WHATSAPP_GROUP_ID=your_group_id_here (optional)
EMAIL_ADDRESS=your_email@gmail.com (optional)
EMAIL_PASSWORD=your_app_password (optional)
EMAIL_RECIPIENT=recipient@gmail.com (optional)
```

---

## 📊 Performance Tracking

The bot logs all signals to SQLite database. Check stats:

```bash
# View recent signals
sqlite3 signals.db "SELECT * FROM signals ORDER BY timestamp DESC LIMIT 10;"

# Get performance stats
curl http://localhost:5000/stats
```

---

## 🔧 Technical Stack

| Component | Technology |
|-----------|------------|
| Data Source | Binance Public API |
| Indicators | TA-Lib (RSI) |
| Alerts | Telegram, WhatsApp, Email |
| Storage | SQLite |
| API | Flask (Health Check) |
| Logging | Python Logger |

---

## 📱 Alert Example

```
🔴 EXTREME OVERBOUGHT

Symbol: BTCUSDT
RSI(5m): 89.50
RSI(15m): 88.30
Price: $45,250.00
Time: 2026-02-19 10:14:48 UTC
```

---

## 🛠️ Commands

- `python main.py` - Start bot
- `python test_alert.py` - Send test alert
- `curl http://localhost:5000/health` - Check bot status
- `curl http://localhost:5000/stats` - Get performance stats

---

## 📝 How It Works

1. **Scans** top 100 USDT pairs by volume
2. **Calculates** RSI on 5m + 15m timeframes
3. **Detects** extreme levels (RSI ≥ 88 or ≤ 12)
4. **Sends** Telegram/WhatsApp/Email alerts
5. **Logs** signals with entry/exit prices
6. **Tracks** performance (win rate, avg return)

---

## ⚙️ Advanced Config

Edit `scanner.py` to customize:

```python
RSI_PERIOD = 14           # RSI calculation period
TOP_COINS_LIMIT = 100     # Scan top X coins
OVERBOUGHT_LEVEL = 88     # RSI threshold
OVERSOLD_LEVEL = 12       # RSI threshold
COOLDOWN_MIN = 40         # Minutes between alerts per coin
TIMEFRAMES = ["5m", "15m"] # Candle timeframes
```

---

## 📊 Example Output

```
2026-02-19 10:13:10 - RSI_Engine - INFO - RSI Extreme Engine started (Public API)
2026-02-19 10:13:10 - RSI_Engine - INFO - Health check server started on port 5000
2026-02-19 10:13:25 - RSI_Engine - WARNING - 🔴 OVERBOUGHT detected: BTCUSDT @ $45250.50
2026-02-19 10:13:26 - RSI_Engine - INFO - ✓ Telegram alert sent for BTCUSDT
2026-02-19 10:13:26 - RSI_Engine - INFO - Signal logged: BTCUSDT overbought RSI(89.50, 88.30) @ 45250.5000
```

---

## 🎯 Roadmap

- [ ] Web dashboard (React)
- [ ] Backtesting module
- [ ] Webhook integration
- [ ] Discord alerts
- [ ] Automated trading (optional)

---

## ⚠️ Disclaimer

This bot is for **educational purposes only**. 

- Not financial advice
- Test thoroughly before using
- Monitor bot activity regularly
- Use at your own risk

---

## 🤝 Contributing

PRs welcome! Report bugs on GitHub Issues.

---

## 📜 License

MIT License © 2026 Drrsee1

---

## 🚀 Get Started Now

**Local:** `python main.py`  
**Cloud:** [Deploy to Replit →](REPLIT_DEPLOYMENT.md)

**Questions?** Open an issue on GitHub or contact @DrRsee1_bot on Telegram!

