from listings.listing_manager import get_listings, renew_listing
from orders.order_manager import get_open_orders, summarize_order
from shared.notifications.notifier import notify
from shared.utils.logger import get_logger

logger = get_logger("etsy-automation", "logs")


def run():
    logger.info("Etsy automation starting...")

    # Report open orders
    orders = get_open_orders()
    if orders:
        summaries = "\n".join(summarize_order(o) for o in orders)
        msg = f"*Etsy Open Orders* ({len(orders)})\n{summaries}"
        logger.info(msg)
        notify(msg, source="Etsy")
    else:
        logger.info("No open orders.")

    # Auto-renew listings expiring soon (quantity = 0)
    listings = get_listings()
    for listing in listings:
        if listing.get("quantity", 1) == 0:
            lid = listing["listing_id"]
            logger.info(f"Renewing listing {lid}")
            renew_listing(lid)


if __name__ == "__main__":
    run()
