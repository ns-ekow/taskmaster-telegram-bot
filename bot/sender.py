from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application
from datetime import datetime
from sheets.roadmap import (
    get_today_tasks,
    get_today_deadlines,
    mark_previous_pending_as_missed,
    update_task_status,
    task_key
)
from config.settings import BOT_TOKEN

# Format a single task nicely
def format_task(task, index):
    resource_links = [link.strip() for link in task["Resource Link"].split(" and ")]
    links_formatted = "\n".join(f"🔗 {link}" for link in resource_links if link)

    text = (
        f"<b>{index}. {task['Topic']}</b>\n"
        f"📖 <i>{task['Subtopic']}</i>\n"
        f"🧠 <b>Focus:</b> {task['Language Focus']}\n"
        f"{links_formatted}\n"
        f"🗓️ <b>Start:</b> {task['Start Date']} | <b>Deadline:</b> {task['Deadline']}\n"
    )

    if task.get("Project Idea") and task["Project Idea"].strip() != "-":
        text += f"🛠️ <b>Project:</b> {task['Project Idea']}\n"
    if task.get("Notes"):
        text += f"📋 <b>Notes:</b> {task['Notes']}\n"

    return text.strip()

# Format the combined message
def build_message(tasks, deadlines):
    lines = []

    if tasks:
        lines.append("📌 <b>New Tasks Starting Today</b>\n")
        for idx, task in enumerate(tasks, 1):
            lines.append(format_task(task, idx))
            lines.append("---")

    if deadlines:
        lines.append("⏰ <b>Deadlines Today</b>")
        for d in deadlines:
            lines.append(f"- {d['Topic']} – {d['Subtopic']} (🗓️ {d['Deadline']})")

    return "\n".join(lines)

# Create inline buttons with callback_data
def create_inline_buttons(tasks):
    buttons = []
    for task in tasks:
        key = task_key(task)
        buttons.append([InlineKeyboardButton(text=f"✅ Done: {task['Topic']}", callback_data=f"done|{key}")])
    return InlineKeyboardMarkup(buttons)

# Send the full message + buttons
async def send_daily_summary(bot_app: Application, chat_id: str):
    try:
        today = datetime.now()
        today_str = today.strftime("%d-%m-%Y")
        print(f"Processing daily summary for {today_str}")

        # Step 1: Mark missed tasks
        mark_previous_pending_as_missed(today)

        # Step 2: Get today's tasks/deadlines
        tasks = get_today_tasks(today_str)
        deadlines = get_today_deadlines(today_str)

        if not tasks and not deadlines:
            print("No tasks or deadlines found for today")
            await bot_app.bot.send_message(chat_id=chat_id, text="No new tasks or deadlines today.")
            return

        # Step 3: Update sheet status to "Pending" for today's tasks
        for t in tasks:
            update_task_status(t["Start Date"], t["Topic"], "Pending")

        # Step 4: Build message
        text = build_message(tasks, deadlines)
        reply_markup = create_inline_buttons(tasks) if tasks else None

        # Validate chat_id
        if not chat_id or not chat_id.strip():
            raise ValueError("Invalid chat_id: Chat ID cannot be empty")

        # Check if text is too long
        if len(text) > 4096:
            print("Warning: Message is too long, truncating...")
            text = text[:4093] + "..."

        print(f"Sending message to chat ID: {chat_id}")

        # Send the message
        try:
            await bot_app.bot.send_message(
                chat_id=chat_id,
                text=text,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            print("Message sent successfully!")
        except Exception as e:
            print(f"Error sending message: {str(e)}")
            # Try sending a simpler message without HTML formatting or buttons
            if "Not Found" in str(e):
                print("Chat ID not found. Please check your Telegram chat ID.")
                raise ValueError(f"Chat ID {chat_id} not found. Please verify your Telegram chat ID is correct.")
            else:
                # Try sending a simpler message
                await bot_app.bot.send_message(
                    chat_id=chat_id,
                    text="Error sending formatted message. Please check the bot's configuration."
                )
    except Exception as e:
        print(f"Error in send_daily_summary: {str(e)}")
        raise
