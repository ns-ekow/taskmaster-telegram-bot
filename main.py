import logging
from datetime import time
import pytz
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler
)
from bot.sender import send_daily_summary
from bot.handler import handle_button
from config.settings import BOT_TOKEN
from deploy_setup import setup_credentials

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set up credentials for deployment
setup_credentials()

# Your Telegram chat ID
# To get your chat ID, send a message to @userinfobot on Telegram
# You need to replace this with your actual chat ID
# For deployment, set the CHAT_ID environment variable
from config.settings import CHAT_ID
YOUR_CHAT_ID = CHAT_ID if CHAT_ID else '1798133963'  # Use environment variable if available

async def send_summary_command(update, context):
    """Handler for the /summary command"""
    chat_id = update.effective_chat.id
    await update.message.reply_text("Generating your daily summary...")
    try:
        await send_daily_summary(context.application, str(chat_id))
    except Exception as e:
        logging.error(f"Error sending summary: {e}")
        await update.message.reply_text(f"Error: {str(e)}")

async def start_command(update, _):
    """Handler for the /start command"""
    await update.message.reply_text(
        "👋 Welcome to the Roadmap Bot!\n\n"
        "I'll send you daily summaries of your tasks and deadlines.\n"
        "Use /summary to get your daily summary now.\n"
        "Use /help to see all available commands."
    )

async def help_command(update, _):
    """Handler for the /help command"""
    await update.message.reply_text(
        "📚 Available commands:\n\n"
        "/start - Start the bot\n"
        "/summary - Get your daily summary\n"
        "/help - Show this help message"
    )

async def scheduled_daily_summary(context):
    """Send the daily summary at scheduled time"""
    try:
        await send_daily_summary(context.application, YOUR_CHAT_ID)
        logging.info("Daily summary sent successfully")
    except Exception as e:
        logging.error(f"Error in scheduled job: {e}")

def main():
    """Run the bot with job queue"""
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("summary", send_summary_command))

    # Add callback query handler for buttons
    application.add_handler(CallbackQueryHandler(handle_button))

    # Schedule daily summary using the built-in job queue
    # Set to run at 6:30 AM GMT+0 (UTC)
    job_queue = application.job_queue
    scheduled_time = time(hour=6, minute=30, tzinfo=pytz.UTC)
    job_queue.run_daily(
        scheduled_daily_summary,
        time=scheduled_time,  # Explicitly set to UTC timezone
        days=(0, 1, 2, 3, 4, 5, 6),  # All days of the week
        name="daily_summary"
    )

    # Log the scheduled time
    logging.info(f"Daily summary scheduled to run at 06:30 AM UTC (GMT+0) every day")

    # Start the bot
    print("Bot running with job queue...")
    application.run_polling()

if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        # Handle graceful shutdown
        logging.info("Bot is shutting down...")
    except Exception as e:
        logging.error(f"Error running bot: {e}")
