from extract import extract_data
from transform import transform_data
from load import load_data
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def run_etl():
    logging.info("ETL started")
    raw = extract_data()
    if not raw:
        logging.info("ETL skipped: No data extracted")
        return
    df = transform_data(raw)
    load_data(df)
    logging.info("ETL finished")

if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(run_etl, 'interval', minutes=5)
    logging.info("Scheduler started. ETL will run every 5 minutes.")
    run_etl()  # First immediate run
    scheduler.start()