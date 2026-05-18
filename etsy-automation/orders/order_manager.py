import requests
from shared.config.config import ETSY_ACCESS_TOKEN, ETSY_SHOP_ID
from shared.utils.logger import get_logger

logger = get_logger("etsy.orders", "etsy-automation/logs")

BASE_URL = "https://openapi.etsy.com/v3/application"
HEADERS = {"Authorization": f"Bearer {ETSY_ACCESS_TOKEN}"}


def get_open_orders() -> list:
    url = f"{BASE_URL}/shops/{ETSY_SHOP_ID}/receipts"
    resp = requests.get(url, headers=HEADERS, params={"was_shipped": False}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Open orders: {data.get('count', 0)}")
    return data.get("results", [])


def summarize_order(order: dict) -> str:
    receipt_id = order.get("receipt_id")
    buyer = order.get("name", "Unknown")
    total = order.get("grandtotal", {}).get("amount", 0) / 100
    items = len(order.get("transactions", []))
    return f"Order #{receipt_id} | Buyer: {buyer} | Items: {items} | Total: ${total:.2f}"
