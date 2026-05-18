import requests
from shared.config.config import ETSY_ACCESS_TOKEN, ETSY_SHOP_ID
from shared.utils.logger import get_logger

logger = get_logger("etsy.listings", "etsy-automation/logs")

BASE_URL = "https://openapi.etsy.com/v3/application"
HEADERS = {
    "Authorization": f"Bearer {ETSY_ACCESS_TOKEN}",
    "Content-Type": "application/json",
}


def get_listings(state: str = "active") -> list:
    url = f"{BASE_URL}/shops/{ETSY_SHOP_ID}/listings"
    resp = requests.get(url, headers=HEADERS, params={"state": state}, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    logger.info(f"Fetched {data.get('count', 0)} listings (state={state})")
    return data.get("results", [])


def update_listing_price(listing_id: int, price: float) -> bool:
    url = f"{BASE_URL}/listings/{listing_id}"
    payload = {"price": str(price)}
    resp = requests.patch(url, headers=HEADERS, json=payload, timeout=10)
    success = resp.status_code == 200
    if success:
        logger.info(f"Updated listing {listing_id} price to ${price}")
    else:
        logger.error(f"Failed to update listing {listing_id}: {resp.text}")
    return success


def renew_listing(listing_id: int) -> bool:
    url = f"{BASE_URL}/shops/{ETSY_SHOP_ID}/listings/{listing_id}/renewal"
    resp = requests.put(url, headers=HEADERS, timeout=10)
    success = resp.status_code == 200
    logger.info(f"Renew listing {listing_id}: {'OK' if success else 'FAILED'}")
    return success
