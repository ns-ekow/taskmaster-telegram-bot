import asyncio
import time
from telegram.ext import ApplicationBuilder
from bot.sender import send_daily_summary
from config.settings import BOT_TOKEN
from google.auth.exceptions import TransportError
from deploy_setup import setup_credentials

# Set up credentials for deployment
setup_credentials()

# Replace with your actual Telegram chat ID
# To get your chat ID, send a message to @userinfobot on Telegram
# For deployment, set the CHAT_ID environment variable
from config.settings import CHAT_ID
YOUR_CHAT_ID = CHAT_ID if CHAT_ID else '1798133963'  # Use environment variable if available

async def test():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add retry logic for Google Sheets connection
    max_retries = 3
    retry_delay = 2  # seconds

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1} of {max_retries}...")
            await send_daily_summary(app, YOUR_CHAT_ID)
            print("Success!")
            break
        except TransportError as e:
            print(f"Google Sheets connection error: {e}")
            if attempt < max_retries - 1:
                print(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print("Max retries reached. Please check your internet connection and Google API access.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

if __name__ == '__main__':
    asyncio.run(test())
