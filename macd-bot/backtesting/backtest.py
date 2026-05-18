import pandas as pd
from strategies.macd_strategy import compute_macd


def backtest(df: pd.DataFrame, initial_capital: float = 1000.0) -> dict:
    df = compute_macd(df.copy())
    df["position"] = 0
    df["position"] = (
        (df["macd"] > df["signal"]).astype(int)
        - (df["macd"] < df["signal"]).astype(int)
    )
    df["returns"] = df["close"].pct_change()
    df["strategy_returns"] = df["position"].shift(1) * df["returns"]

    total_return = df["strategy_returns"].add(1).prod() - 1
    sharpe = (
        df["strategy_returns"].mean() / df["strategy_returns"].std() * (252 ** 0.5)
        if df["strategy_returns"].std() != 0
        else 0
    )
    max_drawdown = (
        df["strategy_returns"].add(1).cumprod()
        / df["strategy_returns"].add(1).cumprod().cummax()
        - 1
    ).min()

    return {
        "total_return_pct": round(total_return * 100, 2),
        "sharpe_ratio": round(sharpe, 3),
        "max_drawdown_pct": round(max_drawdown * 100, 2),
        "final_capital": round(initial_capital * (1 + total_return), 2),
    }
