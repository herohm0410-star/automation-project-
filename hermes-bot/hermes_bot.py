"""
Hermes — a Telegram bot whose "brain" is an OpenAI chat model (GPT/Codex family).

Setup:
    pip install python-telegram-bot openai
    Add to shared/config/secrets.py:
        os.environ["TELEGRAM_BOT_TOKEN"] = "..."
        os.environ["OPENAI_API_KEY"]     = "..."
        os.environ["OPENAI_MODEL"]       = "gpt-4o-mini"   # optional, has a default

Run:
    python -m hermes_bot.hermes_bot
"""

import os
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI

import shared.config.secrets  # noqa: F401  (loads env vars as a side effect)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
logger = logging.getLogger("hermes")

SYSTEM_PROMPT = (
    "You are Hermes, a helpful personal assistant reachable over Telegram. "
    "Be concise and direct."
)

openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")

# Per-chat conversation history, kept small to bound token usage.
HISTORY_LIMIT = 20
conversations: dict[int, list[dict]] = {}


def ask_brain(chat_id: int, user_text: str) -> str:
    history = conversations.setdefault(chat_id, [])
    history.append({"role": "user", "content": user_text})
    history[:] = history[-HISTORY_LIMIT:]

    messages = [{"role": "system", "content": SYSTEM_PROMPT}, *history]
    response = openai_client.chat.completions.create(model=MODEL, messages=messages)
    reply = response.choices[0].message.content

    history.append({"role": "assistant", "content": reply})
    history[:] = history[-HISTORY_LIMIT:]
    return reply


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hermes online. Send me anything.")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    conversations.pop(update.effective_chat.id, None)
    await update.message.reply_text("Conversation cleared.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    user_text = update.message.text
    try:
        reply = ask_brain(chat_id, user_text)
    except Exception:
        logger.exception("Brain call failed")
        reply = "Sorry, I hit an error talking to my brain. Try again in a moment."
    await update.message.reply_text(reply)


def main() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Hermes bot starting (model=%s)", MODEL)
    app.run_polling()


if __name__ == "__main__":
    main()
