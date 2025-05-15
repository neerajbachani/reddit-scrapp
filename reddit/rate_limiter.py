# reddit/rate_limiter.py
import time
from datetime import datetime, timezone
from config.config_loader import get_config
from utils.logger import setup_logger

log = setup_logger()
config = get_config()

class RedditRateLimiter:
    """Simple rolling window limiter — allows up to N requests per 60 seconds."""

    def __init__(self, requests_per_minute=None):
        self.limit = requests_per_minute or config["scraper"]["rate_limit_per_minute"]
        self.window_start = datetime.now(timezone.utc)
        self.request_count = 0
        log.info(f"Rate limiter initialized: {self.limit} requests/minute")

    def wait(self):
        now = datetime.now(timezone.utc)
        elapsed = (now - self.window_start).total_seconds()

        if elapsed > 60:
            # Reset window
            self.window_start = now
            self.request_count = 0
            # No need to wait, we're starting a new window
            self.request_count += 1
            return

        if self.request_count >= self.limit:
            # Calculate how long to wait until the current window ends
            wait_time = max(0.1, 60 - elapsed)
            log.debug(f"Rate limit hit. Sleeping for {wait_time:.2f} seconds...")
            time.sleep(wait_time)
            # Reset window after waiting
            self.window_start = datetime.now(timezone.utc)
            self.request_count = 1  # Count this request
            return

        # If we get here, we're under the limit in the current window
        self.request_count += 1

