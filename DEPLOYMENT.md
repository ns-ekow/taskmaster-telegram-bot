# Deploying the Telegram Roadmap Bot to PythonAnywhere

This guide will walk you through deploying your Telegram Roadmap Bot to [PythonAnywhere](https://www.pythonanywhere.com/), a cloud platform that makes it easy to host and run Python applications.

## Prerequisites

1. A [PythonAnywhere account](https://www.pythonanywhere.com/registration/register/beginner/) (free tier is sufficient)
2. Your bot code pushed to a Git repository (GitHub, GitLab, etc.)
3. Your Google Sheets service account credentials JSON file
4. Your Telegram Bot Token from BotFather
5. Your Telegram Chat ID

## Deployment Steps

### 1. Set Up Your PythonAnywhere Account

1. Sign up for a [PythonAnywhere account](https://www.pythonanywhere.com/registration/register/beginner/) if you don't have one
2. Log in to your PythonAnywhere dashboard

### 2. Clone Your Repository

1. Open a Bash console from your PythonAnywhere dashboard
2. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

### 3. Set Up a Virtual Environment

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

### 4. Upload Service Account Credentials

You have two options for handling your Google Sheets service account credentials:

#### Option 1: Direct Upload

1. In the PythonAnywhere dashboard, go to the "Files" tab
2. Navigate to your project directory
3. Create a `credentials` directory if it doesn't exist
4. Upload your `service_account.json` file to the `credentials` directory
5. Update your `.env` file with the correct path to the service account file

#### Option 2: Base64 Encoding

1. On your local machine, encode your service account JSON file:
   ```bash
   python encode_credentials.py
   ```
2. Copy the base64-encoded string
3. Copy the `.env.example` file to `.env` in your project directory on PythonAnywhere:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file and add your credentials:
   ```
   BOT_TOKEN=your_telegram_bot_token
   SPREADSHEET_ID=your_google_spreadsheet_id
   CHAT_ID=your_telegram_chat_id
   SERVICE_ACCOUNT_JSON_BASE64=your_base64_encoded_string
   ```

### 5. Create a Task for Running the Bot

Since the free tier of PythonAnywhere doesn't allow applications to run indefinitely, you'll need to set up a scheduled task:

1. Go to the "Tasks" tab in your PythonAnywhere dashboard
2. Set up a new scheduled task:
   - Time: Set to run at 6:30 UTC (or your preferred time)
   - Command: Enter the full path to your Python interpreter and script:
     ```
     /home/yourusername/your-repo-name/venv/bin/python /home/yourusername/your-repo-name/main.py
     ```
   - Select "Daily" for the frequency

### 6. Test Your Deployment

1. Run your bot manually to test if everything is working:
   ```bash
   cd /home/yourusername/your-repo-name
   source venv/bin/activate
   python test_bot.py
   ```
2. Check if you receive a message from your bot on Telegram

## Important Notes for PythonAnywhere Free Tier

1. **Task Duration**: On the free tier, tasks can only run for a limited time (about 5-10 minutes). This should be enough for your bot to send daily summaries.

2. **Always-on Applications**: The free tier doesn't support always-on applications. Your bot will only run when the scheduled task executes.

3. **Alternative Approach**: If you need your bot to be more responsive, consider:
   - Upgrading to a paid PythonAnywhere plan
   - Using a webhook-based approach instead of polling (requires code modifications)

## Monitoring and Maintenance

- **Logs**: Check the task log in the PythonAnywhere dashboard after each scheduled run
- **Updates**: When you push changes to your repository, you'll need to pull them on PythonAnywhere:
  ```bash
  cd /home/yourusername/your-repo-name
  git pull
  source venv/bin/activate
  pip install -r requirements.txt
  ```

## Troubleshooting

### Task Not Running

Check the task log for error messages. Common issues include:

- **Path Issues**: Ensure all paths in your task command are correct
- **Environment Variables**: Make sure your `.env` file is properly set up
- **Dependencies**: Verify all required packages are installed in your virtual environment

### Bot Not Sending Messages

If your bot runs but doesn't send messages:

1. Check if your Telegram Bot Token is correct
2. Verify your Chat ID is correct
3. Make sure you've started a conversation with your bot on Telegram

### Google Sheets Connection Issues

If your bot can't connect to Google Sheets:

1. Verify the service account JSON file is correctly uploaded
2. Make sure the spreadsheet ID is correct
3. Confirm you've shared the spreadsheet with the service account email

## Additional Resources

- [PythonAnywhere Documentation](https://help.pythonanywhere.com/)
- [PythonAnywhere API](https://help.pythonanywhere.com/pages/API/)
- [Scheduled Tasks on PythonAnywhere](https://help.pythonanywhere.com/pages/ScheduledTasks/)
