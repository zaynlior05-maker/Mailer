import os
import asyncio
import threading
from flask import Flask, render_template
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes

# Initialize the web app engine
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Initialize Telegram Bot behaviors
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Retrieve the dynamic public URL provided by Railway environment variables
    web_app_url = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")
    if web_app_url and not web_app_url.startswith("http"):
        web_app_url = f"https://{web_app_url}"

    # Fallback placeholder if deployment domain is missing temporarily
    if not web_app_url:
        web_app_url = "https://example.com"

    keyboard = [
        [
            InlineKeyboardButton(
                text="Launch Excel Mailer 🚀",
                web_app={"url": web_app_url}
            )
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text=f"👋 Welcome @{update.effective_user.username or 'User'}\n\n"
             f"Excel Mailer is ready. Use the professional button below to configure mail campaigns.",
        reply_markup=reply_markup
    )

def run_flask():
    # Railway passes the PORT variable automatically
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

def main():
    # Retrieve Bot Token securely from Railway variables
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        print("ERROR: No BOT_TOKEN found in environment variables!")
        return

    # Start Flask Web Server inside a background threat processing line
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Start Telegram Bot Application polling routines
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    
    print("Bot backend and app server are running...")
    application.run_polling()

if __name__ == '__main__':
    main()
