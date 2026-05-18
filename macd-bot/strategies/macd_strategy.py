import pandas as pd
from shared.config.config import MACD_FAST, MACD_SLOW, MACD_SIGNAL


def compute_macd(df: pd.DataFrame) -> pd.DataFrame:
    """Expects df with a 'close' column. Returns df with MACD columns added."""
    ema_fast = df["close"].ewm(span=MACD_FAST, adjust=False).mean()
    ema_slow = df["close"].ewm(span=MACD_SLOW, adjust=False).mean()
    df["macd"] = ema_fast - ema_slow
    df["signal"] = df["macd"].ewm(span=MACD_SIGNAL, adjust=False).mean()
    df["histogram"] = df["macd"] - df["signal"]
    return df


def get_signal(df: pd.DataFrame) -> str:
    """Returns 'buy', 'sell', or 'hold' based on the latest MACD crossover."""
    df = compute_macd(df)
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    if prev["macd"] < prev["signal"] and curr["macd"] > curr["signal"]:
        return "buy"
    elif prev["macd"] > prev["signal"] and curr["macd"] < curr["signal"]:
        return "sell"
    return "hold"
