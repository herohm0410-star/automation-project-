from scrapers.scraper import get_odds
from strategies.kelly import kelly_stake, implied_probability
from shared.config.config import BETTING_BANKROLL
from shared.notifications.notifier import notify
from shared.utils.logger import get_logger

logger = get_logger("sports-betting", "logs")


def run():
    logger.info("Sports betting bot starting...")
    sport = "basketball_nba"

    events = get_odds(sport)
    for event in events:
        home = event.get("home_team")
        away = event.get("away_team")

        for bookmaker in event.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] != "h2h":
                    continue
                for outcome in market["outcomes"]:
                    odds = outcome["price"]
                    prob = implied_probability(odds)
                    stake = kelly_stake(BETTING_BANKROLL, prob, odds)

                    if stake > 0:
                        msg = (
                            f"*Bet signal* | {home} vs {away}\n"
                            f"Outcome: {outcome['name']} @ {odds}\n"
                            f"Stake: ${stake}"
                        )
                        logger.info(msg)
                        notify(msg, source="Sports Betting")


if __name__ == "__main__":
    run()
