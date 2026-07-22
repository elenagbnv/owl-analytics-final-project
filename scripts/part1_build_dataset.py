


import csv
from pathlib import Path
from threading import Thread, Semaphore, Lock
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import requests
import time
import threading
from datetime import datetime, timezone


url = "https://data-api.binance.vision/api/v3/klines"

# clean csv file
output_path = Path("data/clean/clean_market_data.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

# log file
log_path = Path("results/api_download.log")
log_path.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "symbol",
    "interval",
    "open_time",
    "open",
    "high",
    "low",
    "close",
    "volume",
    "close_time",
    "quote_volume",
    "trade_count",
    "taker_buy_base_volume",
    "taker_buy_quote_volume",
]

download_control = Semaphore(100)    # lock for max of 100 API requests at a time

writer_lock = threading.Lock()       # lock to write into the shared CSV

log_lock = threading.Lock()          # lock to ensure only one thread writes into the log file at a time

wait_events_lock = threading.Lock()  # lock needed to ensure the wait event counter can be incremented safely
wait_events_count = 0                # counter to track wait events; accessible globally, read in validation

# configuration params to use for downloading and for validation:
INTERVAL = "1h"
LIMIT = 1000


def log_message(message: str):
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    log_message_line = f"[{timestamp}] [{threading.current_thread().name}] {message}"
    with log_lock:
        with log_path.open("a", encoding="utf-8") as log_file:
            log_file.write(log_message_line + "\n")


def wait_events():
    global wait_events_count
    with wait_events_lock:
        wait_events_count += 1


def get_data(symbol):
        params = {
            "symbol": symbol,
            "interval": INTERVAL,
            "limit": LIMIT,
        }

        # measure the time of acquiring access into serial section
        acquire_start = time.perf_counter()
        download_control.acquire()
        acquire_wait = time.perf_counter() - acquire_start # time waited for access to enter into serial section 

        if acquire_wait > 0.00:  
            wait_events()
            print(f"Rate-limit wait event logged: {symbol} waited {acquire_wait:.2f}s for access")


        
            start = time.perf_counter()                                                      # start time for each request
            log_message(f"START request symbol={symbol} interval={INTERVAL} limit={LIMIT}")  # log message for each request start timestamp
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            end = time.perf_counter()                                                        # end time for each request

            records = response.json()
            records_count = len(records)  # defined BEFORE it's used below (fixes NameError)
            log_message(f"END request symbol={symbol} records={records_count}")
            print(f"Downloaded {symbol}: {records_count} records.")  # logging downloaded count of records for each request

            

            rows = [
                {
                    "symbol": symbol,
                    "interval": INTERVAL,
                    "open_time": record[0],
                    "open": record[1],
                    "high": record[2],
                    "low": record[3],
                    "close": record[4],
                    "volume": record[5],
                    "close_time": record[6],
                    "quote_volume": record[7],
                    "trade_count": record[8],
                    "taker_buy_base_volume": record[9],
                    "taker_buy_quote_volume": record[10],
                }
                for record in records
            ]

            with writer_lock:
                with output_path.open("a", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writerows(rows)

            sleep(60)  # wait for 60 seconds to hold semaphore access for each request before relasing the lock from critical section

            download_control.release()  # releasing semaphore lock after 60 seconds wait to open access into semaphore section (critical section)

### validation ###
def validate_CSV(filepath, symbols, interval, limit):

    # section 1 validation
    print(f"Symbols configured: {len(symbols)}")
    print(f"Interval: {interval}")
    print(f"Limit per symbol: {limit}")
    print(f"Expected records: {len(symbols) * limit}")

    # section 2 validation
    print(f"Created folders: {output_path.parent}, {log_path.parent}")
    print(f"Saved: {filepath}")

    with open(filepath, 'r', newline='') as SCV:  # check that the final dataset has the expected number of records
        reader = csv.reader(SCV)
        next(reader)
        record_count = sum(1 for record in reader)
    print(f"Total records saved: {record_count}")

    log_message(f"WROTE csv= {filepath.name}, {record_count}")

    expected_records = len(symbols) * limit
    if record_count == expected_records:
        print("Record count check: passed")
    else:
        print("Record count check: failed")

    # section 3 validation - printed in Terminal

    # section 4 validation
    print(f"Request limit: {download_control._value} permits available")

    if wait_events_count > 0:
        print(f"Rate-limit wait events logged: {wait_events_count}")
    else:
        print("Rate-limit wait events logged: 0")
    log_message(f"Rate-limit wait events logged: {wait_events_count}")


if __name__ == "__main__":

    symbols = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
        "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT",
    ]

    # writing header for clean_market_data.csv only once:
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    print("Starting multithreaded download for 10 symbols.")
    print("Request limit: 100 requests per minute.")
    print("Current request batch allowed.")

    with ThreadPoolExecutor(max_workers=1000) as executor:
        executor.map(get_data, symbols)
    print("Multithreaded download complete.")

    validate_CSV(output_path, symbols, INTERVAL, LIMIT)  # run validation


   
   


   

   
   




   

   
   

