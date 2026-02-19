import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import EMAIL_ADDRESS, EMAIL_PASSWORD, EMAIL_RECIPIENT
from logger_config import get_logger

logger = get_logger()

def send_email_alert(subject, message):
    """Send email alert"""
    if not EMAIL_ADDRESS or EMAIL_ADDRESS == "your_email@gmail.com":
        logger.debug("Email alerts not configured, skipping")
        return
    
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_RECIPIENT
        msg['Subject'] = subject
        
        msg.attach(MIMEText(message, 'plain'))
        
        # Gmail SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logger.info(f"Email sent: {subject}")
        
    except Exception as e:
        logger.error(f"Error sending email: {e}")
