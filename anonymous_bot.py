import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import datetime
import asyncio
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

BOT_TOKEN = "7990313292:AAGpbAoCErZDUafLMJyZxcZexHjw43l9uyc"
CHAT_ID ="-1002360663415"  # Replace with your group ID
OWNER_ID = 5695137451     # Replace with your Telegram user ID

logging.basicConfig(level=logging.INFO)

# Good morning
async def good_morning_task(app):
    while True:
        now = datetime.datetime.now()
        if now.hour == 6 and now.minute == 0:
            try:
                await app.bot.send_message(chat_id=CHAT_ID, text="🌞 Good Morning, Hackers!")
            except Exception as e:
                print(f"Failed to send message: {e}")
        await asyncio.sleep(60)

# Notify when new member joins
async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for member in update.message.new_chat_members:
        await context.bot.send_message(chat_id=OWNER_ID,
            text=f"👤 Naya member group me: {member.full_name} (@{member.username})")

# Block links
async def block_links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if any(link in update.message.text for link in ["http", "https", "t.me"]):
        try:
            await update.message.delete()
            await update.message.reply_text("🚫 Links are not allowed!")
        except:
            pass

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Anonymous bot ready!")

# Main function
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), block_links))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))

    asyncio.create_task(good_morning_task(app))
    print("Bot is running...")
    await app.run_polling()

# Replit-safe async runner
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped manually.")