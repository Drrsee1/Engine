# 🚀 Replit Deployment Guide

Deploy your RSI Extreme Engine bot to Replit for 24/7 uptime!

## Step 1: Import from GitHub

1. Go to **https://replit.com**
2. Click **"Create Repl"** → **"Import from GitHub"**
3. Paste: `https://github.com/Drrsee1/Engine`
4. Click **"Import"** and wait for it to load

---

## Step 2: Set Environment Variables

1. Click **"Secrets"** (🔒 icon) in the left sidebar
2. Add your keys one by one:

```
TELEGRAM_TOKEN = 8537822695:AAH_mWE06nlG_xXaunleZ1JZdimAqUhhgXw
CHAT_ID = 1726076933
WHATSAPP_GROUP_ID = (optional - your WhatsApp group ID)
EMAIL_ADDRESS = (optional - your Gmail)
EMAIL_PASSWORD = (optional - your Gmail app password)
EMAIL_RECIPIENT = (optional - recipient email)
```

**⚠️ IMPORTANT:** Use Replit Secrets instead of `.env` for security!

---

## Step 3: Install Dependencies

In the terminal, run:

```bash
pip install -r requirements.txt
```

---

## Step 4: Run the Bot

```bash
python main.py
```

Expected output:
```
2026-02-19 10:14:47 - RSI_Engine - INFO - ======================================
2026-02-19 10:14:47 - RSI_Engine - INFO - RSI Extreme Engine started (Public API)
2026-02-19 10:14:47 - RSI_Engine - INFO - Health check server started on port 5000
```

---

## Step 5: Keep It Running 24/7

Replit will auto-stop idle repls. To keep it running:

### Option A: Use Replit's Always On (PAID - $7/month)
- Click **"Tools"** → **"Repl Info"** → Enable **"Always On"**

### Option B: Use UptimeRobot (FREE)
1. Go to **UptimeRobot.com**
2. Create account (free)
3. Add **HTTP Monitor**:
   - URL: Your Replit URL + `/health` 
   - Check frequency: Every 5 minutes
4. This keeps your bot alive!

---

## Step 6: Verify It's Working

1. Check Telegram bot (`@DrRsee1_bot`) for live alerts
2. Visit health endpoint: `https://your-replit-url/health`
3. Check stats: `https://your-replit-url/stats`

---

## What the Bot Does on Replit

✅ Scans top 100 crypto pairs every 5 minutes  
✅ Detects RSI extremes (overbought/oversold)  
✅ Sends Telegram alerts instantly  
✅ Logs signals to SQLite database  
✅ Runs health check API on port 5000  
✅ Zero config after setup!  

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Bot crashes | Check logs in **"Logs"** tab |
| No alerts received | Verify `TELEGRAM_TOKEN` and `CHAT_ID` in Secrets |
| Repl keeps stopping | Enable "Always On" or use UptimeRobot |
| Price/RSI errors | These are normal - bot retries automatically |

---

## Support

- **GitHub**: https://github.com/Drrsee1/Engine
- **Telegram**: @DrRsee1_bot
- Check logs for detailed error messages

---

**Your bot is now running 24/7 in the cloud!** 🎉
