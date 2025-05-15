# Telegram Roadmap Bot

A Telegram bot that sends daily summaries of tasks and deadlines from a Google Sheets roadmap.

## Features

- Daily summaries of tasks starting today
- Notifications about deadlines
- Interactive buttons to mark tasks as done
- Command interface for manual interactions

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- A Google account with access to Google Sheets
- A Telegram account

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd tgbot
```

### Step 2: Set Up a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start a chat with BotFather and send `/newbot`
3. Follow the instructions to create a new bot
4. Once created, BotFather will give you a token. Save this token for the next step.

### Step 4: Set Up Google Sheets API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable the Google Sheets API
4. Create a service account and download the JSON key file
5. Place the JSON key file in the `credentials` directory
6. Share your Google Sheet with the service account email

### Step 5: Configure Environment Variables

1. Copy the `.env.example` file to `.env`
2. Update the `.env` file with your:
   - Telegram Bot Token (from BotFather)
   - Google Sheets Spreadsheet ID
   - Path to the service account JSON file

### Step 6: Get Your Telegram Chat ID

1. Start a conversation with your bot
2. Send a message to [@userinfobot](https://t.me/userinfobot) on Telegram
3. The bot will reply with your chat ID
4. Update the `YOUR_CHAT_ID` variable in `main.py` and `test_bot.py` with your actual chat ID

### Step 7: Test the Bot

Run the test scripts to verify everything is working:

```bash
python test_sheets.py  # Test Google Sheets connection
python test_token.py   # Test Telegram bot token
```

### Step 8: Run the Bot

```bash
python main.py
```

Once the bot is running, you can interact with it by sending commands to your bot on Telegram.

### Step 9: Deploy to Render (Optional)

To deploy the bot to Render:

1. Encode your service account credentials:

   ```bash
   python encode_credentials.py
   ```

2. Follow the instructions in [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment steps.

## Usage

Once the bot is running, you can interact with it using these commands:

- `/start` - Start the bot
- `/help` - Show available commands
- `/summary` - Get your daily summary

## Troubleshooting

### Invalid Token Error

If you see "Invalid token" errors, make sure:

1. You've correctly copied the token from BotFather
2. There are no extra spaces or characters in the token
3. The token is properly set in the `.env` file

### Google Sheets Connection Issues

If you have trouble connecting to Google Sheets:

1. Verify the service account JSON file is in the correct location
2. Make sure the spreadsheet ID is correct
3. Confirm you've shared the spreadsheet with the service account email

### "Chat not found" Error

If you see "Chat not found" errors:

1. Make sure you've updated the `YOUR_CHAT_ID` variable in both `main.py` and `test_bot.py` with your actual Telegram chat ID
2. Ensure you've started a conversation with your bot (send it a message first)
3. The bot can only send messages to users who have initiated a conversation with it
