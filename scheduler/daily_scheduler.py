# scheduler/daily_scheduler.py

import time
from datetime import datetime
from scheduler.schedulers.background import BackgroundScheduler
from scheduler.triggers.cron import CronTrigger
from scheduler.runner import run_daily_pipeline
from utils.logger import setup_logger

log = setup_logger()

def start_scheduler():
    """Start the background scheduler to run the pipeline daily."""
    scheduler = BackgroundScheduler()

    # Run daily at 8:00 AM UTC
    scheduler.add_job(
        run_daily_pipeline,
        trigger=CronTrigger(hour=8, minute=0),
        id="daily_reddit_pipeline",
        name="Daily Reddit Scraping Pipeline",
        replace_existing=True
    )

    scheduler.start()
    log.info("Scheduler started. Pipeline will run daily at 08:00 UTC.")

    try:
        # Keep the main thread alive
        while True:
            time.sleep(3600)  # Sleep for 1 hour
            log.debug(f"Scheduler running. Current time: {datetime.now().isoformat()}")
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()
        log.info("Scheduler shutdown.")

if __name__ == "__main__":
    log.info("Starting scheduler for Reddit scraping pipeline...")
    start_scheduler()
