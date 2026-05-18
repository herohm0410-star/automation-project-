import requests
from shared.config.config import ODDS_API_KEY
from shared.utils.logger import get_logger

logger = get_logger("sports-betting.scraper", "sports-betting/logs")

BASE_URL = "https://api.the-odds-api.com/v4"


def get_sports() -> list:
    url = f"{BASE_URL}/sports"
    resp = requests.get(url, params={"apiKey": ODDS_API_KEY}, timeout=10)
    resp.raise_for_status()
    return resp.json()


def get_odds(sport: str, regions: str = "us", markets: str = "h2h") -> list:
    url = f"{BASE_URL}/sports/{sport}/odds"
    params = {
        "apiKey": ODDS_API_KEY,
        "regions": regions,
        "markets": markets,
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    logger.info(f"Fetched odds for {sport} | {len(resp.json())} events")
    return resp.json()
