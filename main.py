import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackContext,
    ConversationHandler,
    filters
)
from re import match as re_match
import logging
from dotenv import dotenv_values

CONFIG = dotenv_values()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)


def validate_email(email_address: str) -> bool:
    return bool(re_match(
        r"([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)",
        email_address
    ))


EMAIL_ADDRESS, EMAIL_TEXT = range(2)


async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Введите email получателя:")
    return EMAIL_ADDRESS


async def get_address(update: Update, context: CallbackContext) -> int:
    email: str = update.message.text
    if validate_email(email):
        context.user_data["email"] = email
        await update.message.reply_text(
            "Email корректный! Введите текст сообщения:"
        )
        return EMAIL_TEXT
    else:
        await update.message.reply_text(
            "Это некорректный email. Попробуйте снова:"
        )
        return EMAIL_ADDRESS


async def get_text(update: Update, context: CallbackContext) -> int:
    message = update.message.text
    email = context.user_data["email"]
    try:
        send_email(email, message)
        await update.message.reply_text(
            "Сообщение успешно отправлено!",
            # reply_markup=InlineKeyboardMarkup([])
        )
    except Exception as e:
        await update.message.reply_text(f"Ошибка при отправке сообщения: {e}")
    return ConversationHandler.END


def send_email(recipient, text) -> None:
    msg = MIMEMultipart()
    msg["From"] = CONFIG["SENDER_EMAIL"]
    msg["To"] = recipient
    msg["Subject"] = "Сообщение от Telegram-бота"
    msg.attach(MIMEText(text, "plain"))

    # Отправка
    with smtplib.SMTP_SSL(
        host=CONFIG["SMTP_SERVER"],
        port=CONFIG["SMTP_PORT"]
    ) as server:
        server.login(CONFIG["SENDER_EMAIL"], CONFIG["SENDER_PASSWORD"])
        server.sendmail(CONFIG["SENDER_EMAIL"], recipient, msg.as_string())


async def cancel(update: Update, context: CallbackContext):
    await update.message.reply_text("Отмена операции.")
    return ConversationHandler.END


def main():
    app = Application.builder().token(CONFIG["TELEGRAM_TOKEN"]).build()

    # Разговор
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL_ADDRESS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_address)
            ],
            EMAIL_TEXT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, get_text)
            ],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
