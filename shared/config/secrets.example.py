"""
secrets.example.py — API key template.

Setup:
    cp shared/config/secrets.example.py shared/config/secrets.py
    # Fill in your values in secrets.py
    # Import this at the top of any entry point: import shared.config.secrets

secrets.py is gitignored. Never commit real keys.
"""

import os

# ─── Sports Betting ────────────────────────────────────────────────────────────
# The Odds API — https://the-odds-api.com (free tier: 500 req/month)
os.environ["ODDS_API_KEY"] = ""

# Bankroll settings
os.environ["BETTING_BANKROLL"]       = "1000"   # starting bankroll in USD
os.environ["BETTING_MAX_STAKE_PCT"]  = "0.05"   # max 5% per bet (Kelly cap)

# ─── MACD Trading Bot ──────────────────────────────────────────────────────────
# Exchange — uses ccxt (https://github.com/ccxt/ccxt)
# Supported: binance, coinbase, kraken, bybit, kucoin, etc.
os.environ["EXCHANGE_NAME"]       = "binance"
os.environ["EXCHANGE_API_KEY"]    = ""
os.environ["EXCHANGE_API_SECRET"] = ""

# Trading pair and timeframe
os.environ["MACD_TRADING_PAIR"] = "BTC/USDT"
os.environ["MACD_TIMEFRAME"]    = "1h"    # 1m, 5m, 15m, 1h, 4h, 1d

# MACD parameters (standard defaults)
os.environ["MACD_FAST"]   = "12"
os.environ["MACD_SLOW"]   = "26"
os.environ["MACD_SIGNAL"] = "9"

# ─── Etsy ──────────────────────────────────────────────────────────────────────
# Etsy Developer Portal — https://www.etsy.com/developers/your-apps
# Create an app → get API key + secret
os.environ["ETSY_API_KEY"]    = ""
os.environ["ETSY_API_SECRET"] = ""

# Your Etsy shop ID (found in your shop URL or dashboard)
os.environ["ETSY_SHOP_ID"] = ""

# OAuth access token — generated after completing Etsy OAuth flow
# See: https://developers.etsy.com/documentation/tutorials/quickstart
os.environ["ETSY_ACCESS_TOKEN"] = ""

# ─── Notifications ─────────────────────────────────────────────────────────────
# Telegram bot — create via @BotFather on Telegram
# 1. Message @BotFather → /newbot → follow prompts → get token
# 2. Start a chat with your bot, then visit:
#    https://api.telegram.org/bot<TOKEN>/getUpdates to get your chat_id
os.environ["TELEGRAM_BOT_TOKEN"] = ""
os.environ["TELEGRAM_CHAT_ID"]   = ""

# Optional: email for alerts (not yet wired — placeholder for future use)
os.environ["NOTIFICATION_EMAIL"] = ""

# ─── Scheduler ─────────────────────────────────────────────────────────────────
# Override default run times (24h local time, HH:MM)
os.environ["SCHEDULE_MACD"]   = "08:00"
os.environ["SCHEDULE_SPORTS"] = "09:00"
os.environ["SCHEDULE_ETSY"]   = "10:00"
