import requests
from shared.config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(f"[Notifier] Telegram not configured. Message: {message}")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        resp = requests.post(url, json=payload, timeout=10)
        return resp.status_code == 200
    except requests.RequestException as e:
        print(f"[Notifier] Failed to send Telegram message: {e}")
        return False


def notify(message: str, source: str = "") -> None:
    tag = f"[{source}] " if source else ""
    send_telegram(f"{tag}{message}")
