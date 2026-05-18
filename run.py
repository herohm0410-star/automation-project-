"""
Master runner — execute all bots or a specific one.
Usage:
    python run.py              # runs all
    python run.py sports       # sports betting only
    python run.py macd         # MACD bot only
    python run.py etsy         # Etsy automation only
"""
import sys
import os

# Add sub-project roots to path so relative imports work
sys.path.insert(0, os.path.dirname(__file__))


def run_sports():
    sys.path.insert(0, "sports-betting")
    from sports_betting_main import run  # noqa: PLC0415
    run()


def run_macd():
    sys.path.insert(0, "macd-bot")
    from macd_main import run  # noqa: PLC0415
    run()


def run_etsy():
    sys.path.insert(0, "etsy-automation")
    from etsy_main import run  # noqa: PLC0415
    run()


BOTS = {
    "sports": run_sports,
    "macd": run_macd,
    "etsy": run_etsy,
}

if __name__ == "__main__":
    target = sys.argv[1].lower() if len(sys.argv) > 1 else "all"

    if target == "all":
        for name, fn in BOTS.items():
            print(f"\n=== Running {name} ===")
            fn()
    elif target in BOTS:
        BOTS[target]()
    else:
        print(f"Unknown bot: {target}. Choose from: {', '.join(BOTS)} or 'all'")
        sys.exit(1)
