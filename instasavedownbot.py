import os
import asyncio
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import instaloader

# Logging
logging.basicConfig(level=logging.INFO)

# Bot tokenni Render orqali qo‘shamiz (TOKEN env orqali)
TOKEN = os.getenv("7876511816:AAGuZ6kzRqhI3gdYqwRoGINxGvVyvZ7326w")

REQUIRED_CHANNEL = "@Mr_Yahyobek"  # Obuna bo‘lish majburiy kanal

async def check_subscription(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ['member', 'creator', 'administrator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_subscription(user.id, context):
        await update.message.reply_text("🚫 Botdan foydalanish uchun @Mr_Yahyobek kanaliga obuna bo‘ling.")
        return
    await update.message.reply_text("👋 Salom! Instagram link yuboring, yuklab beraman.")

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if not await check_subscription(user.id, context):
        await update.message.reply_text("🚫 Avval @Mr_Yahyobek kanaliga obuna bo‘ling.")
        return

    url = update.message.text
    await update.message.reply_text("📥 Yuklab olinmoqda...")

    loader = instaloader.Instaloader(dirname_pattern="downloads", save_metadata=False)
    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        loader.download_post(post, target=f"{user.id}")
        await update.message.reply_text("✅ Yuklab olindi. Afsuski, Renderda faylni yuborib bo‘lmaydi.")
    except Exception as e:
        await update.message.reply_text(f"❌ Xatolik: {str(e)}")

async def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_instagram))

    print("✅ Bot ishga tushdi...")
    await app.run_polling()

if name == "__main__":
    asyncio.run(main())
