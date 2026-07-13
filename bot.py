import os
import asyncio
import threading
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

app = Flask(__name__)

@app.route('/bank')
def bank_templates():
    return render_template('bank_templates.html')

@app.route('/crypto')
def crypto_templates():
    return render_template('crypto_templates.html')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    web_app_url = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
    if web_app_url and not web_app_url.startswith("http"):
        web_app_url = f"https://{web_app_url}"

    if not web_app_url:
        web_app_url = "https://example.com"

    keyboard = [
        [
            InlineKeyboardButton(
                text="Launch ONYX Mailer 🚀",
                web_app={"url": web_app_url}
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=f"👋 Welcome @{update.effective_user.username or 'User'}\n\n"
             f"The Dynamic Template Engine is ready. Click below to access the library.",
        reply_markup=reply_markup
    )

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("ERROR: No BOT_TOKEN found in environment variables!")
        return

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("System running with Dynamic Template Engine...")
    application.run_polling()

if __name__ == '__main__':
    main()
