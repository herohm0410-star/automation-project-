"""
Daily scheduler — runs all three bots on a fixed schedule.
Start it once; it keeps running in the background.

Default times (24h, local time):
    Sports betting : 09:00
    MACD bot       : 08:00
    Etsy           : 10:00

Override via env vars:
    SCHEDULE_SPORTS=09:00
    SCHEDULE_MACD=08:00
    SCHEDULE_ETSY=10:00
"""

import os
import sys
import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("scheduler")

ROOT = os.path.dirname(__file__)


def _run_sports():
    sys.path.insert(0, os.path.join(ROOT, "sports-betting"))
    import importlib, main as m  # noqa: E401
    importlib.reload(m)
    m.run()


def _run_macd():
    sys.path.insert(0, os.path.join(ROOT, "macd-bot"))
    import importlib, main as m  # noqa: E401
    importlib.reload(m)
    m.run()


def _run_etsy():
    sys.path.insert(0, os.path.join(ROOT, "etsy-automation"))
    import importlib, main as m  # noqa: E401
    importlib.reload(m)
    m.run()


def _parse_time(env_var: str, default: str) -> tuple[int, int]:
    raw = os.getenv(env_var, default)
    h, m = raw.split(":")
    return int(h), int(m)


def main():
    scheduler = BlockingScheduler(timezone="local")

    sports_h, sports_m = _parse_time("SCHEDULE_SPORTS", "09:00")
    macd_h,   macd_m   = _parse_time("SCHEDULE_MACD",   "08:00")
    etsy_h,   etsy_m   = _parse_time("SCHEDULE_ETSY",   "10:00")

    scheduler.add_job(
        _run_sports,
        CronTrigger(hour=sports_h, minute=sports_m),
        id="sports-betting",
        name="Sports Betting Bot",
        misfire_grace_time=300,
    )
    scheduler.add_job(
        _run_macd,
        CronTrigger(hour=macd_h, minute=macd_m),
        id="macd-bot",
        name="MACD Bot",
        misfire_grace_time=300,
    )
    scheduler.add_job(
        _run_etsy,
        CronTrigger(hour=etsy_h, minute=etsy_m),
        id="etsy-automation",
        name="Etsy Automation",
        misfire_grace_time=300,
    )

    logger.info(
        f"Scheduler started — "
        f"Sports@{sports_h:02d}:{sports_m:02d} | "
        f"MACD@{macd_h:02d}:{macd_m:02d} | "
        f"Etsy@{etsy_h:02d}:{etsy_m:02d}"
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
