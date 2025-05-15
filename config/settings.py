import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables with validation
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logging.error("BOT_TOKEN not found in environment variables")
    raise ValueError("BOT_TOKEN environment variable is required")

# Fix escape characters in the token if present
if r'\x3a' in BOT_TOKEN:
    BOT_TOKEN = BOT_TOKEN.replace(r'\x3a', ':')
    logging.warning("Fixed escape character in BOT_TOKEN")

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
if not SPREADSHEET_ID:
    logging.error("SPREADSHEET_ID not found in environment variables")
    raise ValueError("SPREADSHEET_ID environment variable is required")

SERVICE_ACCOUNT_PATH = os.getenv("SERVICE_ACCOUNT_PATH")
if not SERVICE_ACCOUNT_PATH:
    logging.error("SERVICE_ACCOUNT_PATH not found in environment variables")
    raise ValueError("SERVICE_ACCOUNT_PATH environment variable is required")

# Get chat ID from environment (for deployment)
CHAT_ID = os.getenv("CHAT_ID")
if CHAT_ID:
    logging.info(f"Using CHAT_ID from environment variable")

# Print settings for debugging (without exposing the full token)
token_preview = BOT_TOKEN[:8] + "..." if BOT_TOKEN else "None"
logging.info(f"BOT_TOKEN: {token_preview}")
logging.info(f"SPREADSHEET_ID: {SPREADSHEET_ID}")
logging.info(f"SERVICE_ACCOUNT_PATH: {SERVICE_ACCOUNT_PATH}")
if CHAT_ID:
    logging.info(f"CHAT_ID: {CHAT_ID}")
