import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Create logger
logger = logging.getLogger("RSI_Engine")
logger.setLevel(logging.DEBUG)

# File handler - logs to file
file_handler = logging.FileHandler(f"logs/engine_{datetime.utcnow().strftime('%Y%m%d')}.log")
file_handler.setLevel(logging.DEBUG)

# Console handler - logs to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def get_logger():
    return logger
