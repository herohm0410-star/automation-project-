from shared.config.config import BETTING_BANKROLL, BETTING_MAX_STAKE_PCT


def kelly_stake(bankroll: float, win_prob: float, decimal_odds: float) -> float:
    """Kelly Criterion: returns recommended stake amount."""
    b = decimal_odds - 1
    q = 1 - win_prob
    fraction = (b * win_prob - q) / b
    fraction = max(0.0, fraction)  # never negative
    fraction = min(fraction, BETTING_MAX_STAKE_PCT)  # cap exposure
    return round(bankroll * fraction, 2)


def implied_probability(decimal_odds: float) -> float:
    return 1 / decimal_odds
