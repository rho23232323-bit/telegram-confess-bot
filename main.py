from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import time
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

last_confession = {}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    now = time.time()

    if user_id in last_confession:
        if now - last_confession[user_id] < 86400:
            await update.message.reply_text("⏳ You can only confess once every 24 hours.")
            return

    confession = update.message.text
    last_confession[user_id] = now

    post_text = f"🖤 Anonymous Confession:\n\n{confession}"

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=post_text
    )

    await update.message.reply_text("✅ Your confession has been posted.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()