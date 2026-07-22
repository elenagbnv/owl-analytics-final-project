

import csv
from pathlib import Path
from threading import Thread, Semaphore, Lock
from concurrent.futures import ThreadPoolExecutor
from time import sleep
import requests
import time
import threading

url = "https://data-api.binance.vision/api/v3/klines"

output_path = Path("data/clean/clean_market_data.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)

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

dowload_control= Semaphore (100)    # max of 100 API requests per minute
writer_lock = threading.Lock()      # lock to write into the shared CSV


def get_data(symbol):
        params = {
            "symbol": symbol,
            "interval": "1h",
            "limit": 1000,
        }
        with dowload_control:
            start = time.perf_counter()                                     # logging wait time #start
            sleep(60)                                                       # wait time detected
            end = time.perf_counter()                                       # logging wait time #end
            print(f"Rate-limit wait event logged: {end - start:.2f}s ")     # logging wait time: Rate-limit wait event logged: 60.00s x10
          
            start = time.perf_counter()                             # log time for each symbol #start
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            end = time.perf_counter()                               # log time for each symbol #end 
            print(f"Downloaded {symbol}: 1000 records.")  
            print(f"Download time for {symbol}: {end - start:.2f}s") # logging download time for each symbol 
            records = response.json()  
            
            rows = [
                {
                    "symbol": symbol,
                    "interval": "1h",
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
        
if __name__ == "__main__":
    
    symbols = [
        "BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT",
        "ADAUSDT", "DOGEUSDT", "AVAXUSDT", "LINKUSDT", "DOTUSDT",
    ]

    # writing header for the output file only once:
    with output_path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

    print("Starting multithreaded download for 10 symbols.") # 1 worked
    print("Request limit: 100 requests per minute.") # 2 worked
    print("Current request batch allowed.") # 3 worked

    with ThreadPoolExecutor(max_workers=1000) as executor:
         executor.map(get_data, symbols)
    print("Multithreaded download complete.")
   

   
   


   

   
   




   

   
   

