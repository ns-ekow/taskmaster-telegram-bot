from telegram import Update
from telegram.ext import CallbackContext
from sheets.roadmap import update_task_status

# Handle inline button presses
async def handle_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    data = query.data
    if not data.startswith("done|"):
        await query.edit_message_text("Unknown action.")
        return

    _, key = data.split("|", 1)
    try:
        start_date, topic = key.split("::", 1)
    except ValueError:
        await query.edit_message_text("Invalid key format.")
        return

    success = update_task_status(start_date, topic, "Done")
    if success:
        await query.edit_message_text(f"✅ Marked '{topic}' as done!")
    else:
        await query.edit_message_text("⚠️ Could not update the task. Please try again.")
