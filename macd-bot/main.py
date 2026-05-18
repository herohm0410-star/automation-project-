import ccxt
import pandas as pd
from strategies.macd_strategy import get_signal
from shared.config.config import (
    EXCHANGE_NAME, EXCHANGE_API_KEY, EXCHANGE_API_SECRET,
    MACD_TRADING_PAIR, MACD_TIMEFRAME,
)
from shared.notifications.notifier import notify
from shared.utils.logger import get_logger

logger = get_logger("macd-bot", "logs")


def fetch_ohlcv() -> pd.DataFrame:
    exchange_class = getattr(ccxt, EXCHANGE_NAME)
    exchange = exchange_class({"apiKey": EXCHANGE_API_KEY, "secret": EXCHANGE_API_SECRET})
    raw = exchange.fetch_ohlcv(MACD_TRADING_PAIR, timeframe=MACD_TIMEFRAME, limit=100)
    df = pd.DataFrame(raw, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    return df


def run():
    logger.info(f"MACD bot starting | {MACD_TRADING_PAIR} {MACD_TIMEFRAME}")
    df = fetch_ohlcv()
    signal = get_signal(df)

    logger.info(f"Signal: {signal.upper()}")
    if signal in ("buy", "sell"):
        msg = f"*MACD Signal* | {MACD_TRADING_PAIR}\nAction: `{signal.upper()}`"
        notify(msg, source="MACD Bot")


if __name__ == "__main__":
    run()
