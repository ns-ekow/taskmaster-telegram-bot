import asyncio
import logging
import sys
import os
from telegram import Bot
from dotenv import load_dotenv

# Set up logging to console
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Set to DEBUG for more verbose output
    handlers=[logging.StreamHandler(sys.stdout)]
)

async def test_token():
    """Test if the bot token is valid"""
    print("=== ENV FILE TOKEN TEST ===")

    # Load .env file directly
    print("Loading .env file...")
    load_dotenv(verbose=True)

    # Get token from environment
    bot_token = os.getenv("BOT_TOKEN")

    # Debug information
    print(f"Environment variable BOT_TOKEN: {bot_token}")
    if bot_token:
        print(f"Token length: {len(bot_token)}")
        print(f"Token format check: {'PASSED' if ':' in bot_token else 'FAILED'}")
    else:
        print("❌ BOT_TOKEN environment variable is not set or is empty")
        return False

    try:
        # Create a bot instance
        print("Creating Bot instance...")
        bot = Bot(token=bot_token)

        # Try to get bot information
        print(f"Testing bot token: {bot_token[:8]}...")
        print("Calling bot.get_me()...")
        bot_info = await bot.get_me()

        # Print bot information
        print(f"✅ Token is valid!")
        print(f"Bot username: @{bot_info.username}")
        print(f"Bot name: {bot_info.first_name}")
        print(f"Bot ID: {bot_info.id}")
        return True
    except Exception as e:
        print(f"❌ Token validation failed: {e}")
        print(f"Token used: {bot_token}")
        print(f"Exception type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_token())
    print(f"Test result: {'SUCCESS' if success else 'FAILURE'}")
    exit(0 if success else 1)
