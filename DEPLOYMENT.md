# Deploying the Telegram Roadmap Bot to Render

This guide will walk you through deploying your Telegram Roadmap Bot to [Render](https://render.com), a cloud platform that makes it easy to deploy applications.

## Prerequisites

1. A [Render account](https://dashboard.render.com/register)
2. Your bot code pushed to a Git repository (GitHub, GitLab, etc.)
3. Your Google Sheets service account credentials JSON file
4. Your Telegram Bot Token from BotFather
5. Your Telegram Chat ID

## Deployment Steps

### 1. Prepare Your Repository

Make sure your repository includes:

- All the bot code
- `requirements.txt` file
- `render.yaml` file (for Blueprint deployment)
- `.gitignore` file (to exclude sensitive files)

### 2. Create a New Web Service on Render

1. Log in to your [Render Dashboard](https://dashboard.render.com/)
2. Click on the "New +" button and select "Background Worker"
3. Connect your Git repository
4. Configure your service:
   - **Name**: `telegram-roadmap-bot` (or any name you prefer)
   - **Environment**: `Python`
   - **Region**: Choose the region closest to you
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`
   - **Plan**: Free (or select a paid plan if you need more resources)

### 3. Set Environment Variables

In the Render dashboard, add the following environment variables:

- `BOT_TOKEN`: Your Telegram Bot Token
- `SPREADSHEET_ID`: Your Google Sheets Spreadsheet ID
- `CHAT_ID`: Your Telegram Chat ID

Note: The bot is configured to send daily summaries at 6:30 AM GMT+0 (UTC) time. If you need to change this, modify the `scheduled_time` variable in `main.py`.

### 4. Upload Service Account Credentials

Since Render doesn't support uploading files directly, you have two options:

#### Option 1: Use Render's Secret Files

1. In your service settings, go to the "Secret Files" section
2. Add a new secret file:
   - **Filename**: `credentials/service_account.json`
   - **Contents**: Paste the entire contents of your service account JSON file
3. Update your `SERVICE_ACCOUNT_PATH` environment variable to point to this location

#### Option 2: Encode as Environment Variable

1. Base64 encode your service account JSON file:
   ```bash
   cat credentials/service_account.json | base64
   ```
2. Add a new environment variable:
   - **Key**: `SERVICE_ACCOUNT_JSON_BASE64`
   - **Value**: The base64-encoded string
3. Modify your code to decode this at runtime:

   ```python
   # Add to your main.py or a startup script
   import base64
   import os
   import json

   # Create credentials directory if it doesn't exist
   os.makedirs('credentials', exist_ok=True)

   # Decode and save the service account JSON
   if 'SERVICE_ACCOUNT_JSON_BASE64' in os.environ:
       json_data = base64.b64decode(os.environ['SERVICE_ACCOUNT_JSON_BASE64']).decode('utf-8')
       with open('credentials/service_account.json', 'w') as f:
           f.write(json_data)
   ```

### 5. Deploy Your Service

1. Click "Create Background Worker"
2. Wait for the deployment to complete
3. Check the logs to make sure your bot starts successfully

## Monitoring and Maintenance

- **Logs**: Monitor your bot's logs in the Render dashboard
- **Updates**: When you push changes to your repository, Render will automatically redeploy your bot (if auto-deploy is enabled)
- **Scaling**: If needed, you can upgrade your plan for more resources

## Troubleshooting

### Bot Not Starting

Check the logs for error messages. Common issues include:

- **Missing Environment Variables**: Ensure all required environment variables are set
- **Service Account Issues**: Verify the service account JSON file is correctly set up
- **Network Issues**: Check if the bot can connect to the Telegram API and Google Sheets API

### Bot Crashes

If your bot crashes frequently:

1. Implement better error handling in your code
2. Consider adding a process manager like Supervisor
3. Upgrade to a paid plan for more reliable performance

## Additional Resources

- [Render Documentation](https://render.com/docs)
- [Python on Render](https://render.com/docs/python)
- [Environment Variables on Render](https://render.com/docs/environment-variables)
- [Secret Files on Render](https://render.com/docs/secret-files)
