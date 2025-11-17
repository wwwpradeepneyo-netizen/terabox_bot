from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import subprocess
import os

BOT_TOKEN = "8542692982:AAFTK9pV_5RTMISGtw7DwBsahfTF7rlUcVE"

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "terabox.com" not in url:
        await update.message.reply_text("Send a valid TeraBox link.")
        return

    await update.message.reply_text("Downloading... Please wait ⏳")

    try:
        result = subprocess.run(
            ["terabox", url],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if "Downloaded:" in output:
            file_path = output.split("Downloaded:")[-1].strip()

            if os.path.exists(file_path):
                await update.message.reply_document(open(file_path, "rb"))
                return

        await update.message.reply_text("Download failed ❌")

    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
