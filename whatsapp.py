import pywhatkit as kit
from config import WHATSAPP_GROUP_ID
import time

def send_whatsapp_message(message):
    """
    Send message to WhatsApp group
    Note: Your computer/phone screen must be unlocked when message is sent
    pywhatkit will open WhatsApp Web automatically
    """
    try:
        # Schedule message to send after 3 seconds (gives time for WhatsApp to load)
        current_time = time.localtime()
        hour = current_time.tm_hour
        minute = current_time.tm_min + 1  # Send 1 minute from now
        
        if minute >= 60:
            hour += 1
            minute = 0
        
        # Send to group using group ID
        kit.sendwhatmsg_to_group(WHATSAPP_GROUP_ID, message, hour, minute)
        print(f"✓ WhatsApp message queued to {WHATSAPP_GROUP_ID}")
    except Exception as e:
        print(f"✗ WhatsApp Error: {e}")
