#!/usr/bin/env python3
"""
Test script to send a fake alert to verify Telegram and WhatsApp notifications
"""

import sys
sys.path.insert(0, '/workspaces/Engine')

from telegram import send_message
from signal_logger import log_signal
from logger_config import get_logger

logger = get_logger()

def test_alert():
    """Send a test alert"""
    
    test_symbol = "BTCUSDT"
    test_signal = "overbought"
    test_rsi_values = [89.5, 88.3]  # Fake RSI values
    test_price = 45250.50
    
    logger.info("=" * 60)
    logger.warning("🧪 SENDING TEST ALERT 🧪")
    logger.info("=" * 60)
    
    print("\n📤 Sending test notification...")
    print(f"   Symbol: {test_symbol}")
    print(f"   Signal: {test_signal.upper()}")
    print(f"   RSI(5m): {test_rsi_values[0]:.2f}")
    print(f"   RSI(15m): {test_rsi_values[1]:.2f}")
    print(f"   Price: ${test_price:.2f}")
    print("\n📨 Sending to Telegram and WhatsApp...")
    
    try:
        # Send test message
        send_message(test_symbol, test_signal, test_rsi_values, test_price)
        logger.info("✓ Test alerts sent successfully!")
        
        # Log to database
        log_signal(test_symbol, test_signal, test_rsi_values, test_price)
        logger.info("✓ Test signal logged to database!")
        
        print("\n✅ TEST ALERT SENT!")
        print("   Check your Telegram bot: @DrRsee1_bot")
        print("   Check your WhatsApp group (if configured)")
        print("   Check your email (if configured)")
        
    except Exception as e:
        logger.error(f"✗ Error sending test alert: {e}")
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_alert()
