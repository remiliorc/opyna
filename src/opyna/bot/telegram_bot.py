"""Bot de Telegram (stub).

Arranca con:
    python -m opyna.bot.telegram_bot
Requiere TELEGRAM_BOT_TOKEN en .env.
"""
from __future__ import annotations

from opyna.settings import settings


def main() -> None:
    if not settings.telegram_bot_token:
        raise SystemExit("Falta TELEGRAM_BOT_TOKEN en .env")

    from telegram.ext import Application, CommandHandler, ContextTypes
    from telegram import Update

    async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE) -> None:
        await update.message.reply_text(
            "Hola, soy Opyna. Envíame una reseña y te digo el sentimiento por aspecto."
        )

    app = Application.builder().token(settings.telegram_bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()


if __name__ == "__main__":
    main()
