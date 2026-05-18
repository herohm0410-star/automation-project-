import os

# --- Sports Betting ---
ODDS_API_KEY = os.getenv("ODDS_API_KEY", "")
BETTING_BANKROLL = float(os.getenv("BETTING_BANKROLL", "1000"))
BETTING_MAX_STAKE_PCT = float(os.getenv("BETTING_MAX_STAKE_PCT", "0.05"))  # 5% of bankroll

# --- MACD Bot ---
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
EXCHANGE_API_SECRET = os.getenv("EXCHANGE_API_SECRET", "")
EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "binance")  # ccxt exchange id
MACD_TRADING_PAIR = os.getenv("MACD_TRADING_PAIR", "BTC/USDT")
MACD_TIMEFRAME = os.getenv("MACD_TIMEFRAME", "1h")
MACD_FAST = int(os.getenv("MACD_FAST", "12"))
MACD_SLOW = int(os.getenv("MACD_SLOW", "26"))
MACD_SIGNAL = int(os.getenv("MACD_SIGNAL", "9"))

# --- Etsy ---
ETSY_API_KEY = os.getenv("ETSY_API_KEY", "")
ETSY_API_SECRET = os.getenv("ETSY_API_SECRET", "")
ETSY_SHOP_ID = os.getenv("ETSY_SHOP_ID", "")
ETSY_ACCESS_TOKEN = os.getenv("ETSY_ACCESS_TOKEN", "")

# --- Notifications ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")
