import requests
from config import TELEGRAM_TOKEN, CHAT_ID, WHATSAPP_GROUP_ID
from logger_config import get_logger

logger = get_logger()

def send_message(symbol, signal_type, rsi_values, current_price):
    """
    Send message to Telegram and WhatsApp
    rsi_values: list of RSI values [rsi_5m, rsi_15m, ...]
    """
    try:
        # Format RSI values
        rsi_text = ""
        timeframes = ["5m", "15m"]
        for i, tf in enumerate(timeframes):
            if i < len(rsi_values):
                rsi_text += f"RSI({tf}): {rsi_values[i]:.2f}\n"
        
        signal_emoji = "🔴" if signal_type == "overbought" else "🟢"
        signal_text = "EXTREME OVERBOUGHT" if signal_type == "overbought" else "EXTREME OVERSOLD"
        
        message = f"""{signal_emoji} {signal_text}

Symbol: {symbol}
{rsi_text}
Price: ${current_price:.4f}
Time: {__import__('datetime').datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
        
        # Send to Telegram
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
            payload = {"chat_id": CHAT_ID, "text": message}
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                logger.info(f"✓ Telegram alert sent for {symbol}")
            else:
                logger.error(f"✗ Telegram error: {response.status_code} - {response.text}")
        except Exception as e:
            logger.error(f"✗ Telegram Error: {e}")
        
        # Send to WhatsApp if configured
        if WHATSAPP_GROUP_ID and WHATSAPP_GROUP_ID != "your_whatsapp_group_id_here":
            try:
                from whatsapp import send_whatsapp_message
                send_whatsapp_message(message)
                logger.info(f"✓ WhatsApp alert sent for {symbol}")
            except ImportError:
                logger.debug("WhatsApp module not configured")
            except Exception as e:
                logger.warning(f"WhatsApp Error: {e}")
        
        # Send email alert if configured
        try:
            from config import EMAIL_ADDRESS
            if EMAIL_ADDRESS and EMAIL_ADDRESS != "your_email@gmail.com":
                from email_sender import send_email_alert
                send_email_alert(f"RSI Alert: {symbol} {signal_text}", message)
        except Exception as e:
            logger.debug(f"Email not configured: {e}")
            
    except Exception as e:
        logger.error(f"Error in send_message: {e}")

