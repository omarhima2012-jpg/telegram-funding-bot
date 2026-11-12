
import os
import sqlite3
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes
)

TOKEN = os.getenv("BOT_TOKEN")

db = sqlite3.connect("bot.db", check_same_thread=False)
db.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0
)
""")
db.commit()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (user.id,)
    )
    db.commit()

    await update.message.reply_text(
        f"أهلاً {user.first_name} 🌟\n"
        "مرحباً بك في بوت النقاط والتمويل الاختياري.\n\n"
        "/balance - رصيدي\n"
        "/help - المساعدة"
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    row = db.execute(
        "SELECT points FROM users WHERE user_id=?",
        (user_id,)
    ).fetchone()

    points = row[0] if row else 0
    await update.message.reply_text(
        f"رصيدك الحالي: {points} نقطة 💰"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "أوامر البوت:\n"
        "/start - تشغيل البوت\n"
        "/balance - عرض النقاط\n"
        "/help - المساعدة\n\n"
        "الانضمام للقنوات يتم باختيار العضو وموافقته."
    )


def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is missing")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("balance", balance))
    app.add_handler(CommandHandler("help", help_command))
    app.run_polling()


if __name__ == "__main__":
    main()
