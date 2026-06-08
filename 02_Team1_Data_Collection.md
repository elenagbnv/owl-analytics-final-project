# Team 1: Data Collection

Team lead: **Elena**

Elena gives you your first task:

> "We need a reliable script that downloads market data. The API is public, but please do not send too many requests at the same time. Also, I want a proper log file because we need to know what happened if something fails."

## First Step: Run the Starter Scripts

Before you build the full downloader, run the two small starter scripts.

First, run the API example:

```bash
python scripts/get_one_record.py
```

This script downloads one `BTCUSDT` record and saves it as:

```txt
data/clean/one_record.csv
```

Then run the dictionary-to-CSV example:

```bash
python scripts/save_dictionary_to_csv.py
```

This script saves one Python dictionary as:

```txt
data/clean/example_dictionary_row.csv
```

Open both scripts and read them carefully. Together, they show the basic ideas you will reuse in your own `part1_build_dataset.py`: call the API, read the response, map the fields into dictionaries, and write CSV rows.

## API

You will use the Binance public market data API to extract data.

Endpoint:

```txt
https://data-api.binance.vision/api/v3/klines
```

Example request:

```txt
https://data-api.binance.vision/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=1000
```

The `limit` parameter controls how many kline records the API returns for one symbol. In `scripts/get_one_record.py`, `limit=1` is used only to test the API with one row. In your full downloader, use `limit=1000`. Binance documents `1000` as the maximum `limit` for this kline endpoint, so one request can return up to 1,000 records for one symbol.

Useful documentation:

- [Binance Spot REST API documentation](https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md)
- [Binance market-data-only FAQ](https://github.com/binance/binance-spot-api-docs/blob/master/faqs/market_data_only.md)

If the Binance API is unavailable, ask your instructor before switching API.

## Dataset Specification

Use these ten symbols:

- `BTCUSDT`
- `ETHUSDT`
- `BNBUSDT`
- `SOLUSDT`
- `XRPUSDT`
- `ADAUSDT`
- `DOGEUSDT`
- `AVAXUSDT`
- `LINKUSDT`
- `DOTUSDT`

Use:

- `interval=1h`
- `limit=1000`

This means your downloader should make one request per symbol.

Expected dataset size:

- 10 symbols
- 1,000 records per symbol
- 10,000 records total
- 1 header row in the CSV
- 10,001 lines total in `data/clean/clean_market_data.csv`

The 10,000 records are a mixed collection of market candles across 10 symbols and 1,000 timestamps per symbol.

## Required Columns

Field mapping:

| CSV column | Value |
| --- | --- |
| `symbol` | the symbol you requested, for example `BTCUSDT` |
| `interval` | the interval you requested, `1h` |
| `open_time` | `record[0]`, converted to a readable timestamp if possible |
| `open` | `record[1]` |
| `high` | `record[2]` |
| `low` | `record[3]` |
| `close` | `record[4]` |
| `volume` | `record[5]` |
| `close_time` | `record[6]`, converted to a readable timestamp if possible |
| `quote_volume` | `record[7]` |
| `trade_count` | `record[8]` |
| `taker_buy_base_volume` | `record[9]` |
| `taker_buy_quote_volume` | `record[10]` |

Example dataset sample:

| symbol | interval | open_time | open | high | low | close | volume | close_time | quote_volume | trade_count |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- | ---: | ---: |
| BTCUSDT | 1h | 2026-05-28T00:00:00+00:00 | 108742.01 | 109120.44 | 108330.50 | 108990.32 | 1284.52 | 2026-05-28T00:59:59+00:00 | 139957223.15 | 84231 |
| ETHUSDT | 1h | 2026-05-28T00:00:00+00:00 | 2638.22 | 2661.40 | 2625.12 | 2654.77 | 18452.83 | 2026-05-28T00:59:59+00:00 | 48978103.62 | 53480 |
| SOLUSDT | 1h | 2026-05-28T00:00:00+00:00 | 168.45 | 170.10 | 167.88 | 169.72 | 93211.14 | 2026-05-28T00:59:59+00:00 | 15796231.88 | 42190 |

Create:

```txt
part1_build_dataset.py
```

Your script must create:

```txt
data/clean/clean_market_data.csv
results/api_download.log
results/runtime_comparison.csv
```

Your script should create the `data/clean/` and `results/` folders automatically if they do not already exist.

## Requirements

Team 1 is worth **25 marks**.

Your script must complete these tasks:

1. Use the correct API settings. Download data for exactly these symbols: `BTCUSDT`, `ETHUSDT`, `BNBUSDT`, `SOLUSDT`, `XRPUSDT`, `ADAUSDT`, `DOGEUSDT`, `AVAXUSDT`, `LINKUSDT`, and `DOTUSDT`. Use `interval=1h` and `limit=1000` for each symbol. **4 marks**

2. Create one combined CSV dataset with exactly 10,000 records. Save it as `data/clean/clean_market_data.csv`, print the number of records saved, and check that the final dataset has 10,000 records. Your script should create the required folders automatically if they do not already exist. **4 marks**

3. Use multithreading to download API data. Your code should show that multiple API downloads can be started without waiting for each symbol to finish one by one. **4 marks**

4. Control the API request rate. Use a synchronization method to limit how many API requests can run at the same time, and limit the downloader to a maximum of 100 API requests per minute. If the downloader has to wait because of the request-per-minute limit, log that wait. **3 marks**

5. Write a reliable log file. Use a lock so that only one thread writes to the log file at a time. Log when each request starts, when each request finishes, how many records were received for each symbol, and when the final CSV is written. **4 marks**

6. Add a benchmark that compares serial API downloading with multithreaded API downloading. The benchmark must compare the download step only and save the result as `results/runtime_comparison.csv`. **4 marks**

7. Keep the script clear and easy to run. Use clear terminal output, sensible file paths, and readable code structure. **2 marks**

## Multithreading benchmark

Elena also asks:

> "Before you move to the next team, compare serial API downloading with multithreaded API downloading. I want you to understand when threads help and when thread overhead makes them slower."

Add a small benchmark that compares:

1. serial API downloading
2. multithreaded API downloading with `ThreadPoolExecutor`

Use `time.perf_counter()`.

This benchmark should compare the download step only. Do not add price calculations or analytics in Team 1; those belong to Team 2 and Team 3.

## Example outputs

Your exact numbers will be different because market data changes, but your output should have this shape.

Example terminal output:

```txt
Starting download for 10 symbols...
Downloaded BTCUSDT: 1000 records
Downloaded ETHUSDT: 1000 records
Downloaded BNBUSDT: 1000 records
Downloaded SOLUSDT: 1000 records
Downloaded XRPUSDT: 1000 records
Downloaded ADAUSDT: 1000 records
Downloaded DOGEUSDT: 1000 records
Downloaded AVAXUSDT: 1000 records
Downloaded LINKUSDT: 1000 records
Downloaded DOTUSDT: 1000 records

Saved clean_market_data.csv
Total records saved: 10000

Runtime comparison
serial_seconds: 105.1999
multithreading_seconds: 49.2628
Fastest method: multithreading
```

Example log file lines:

```txt
2026-06-07T09:11:44Z | START request symbol=BTCUSDT interval=1h limit=1000
2026-06-07T09:11:50Z | END request symbol=BTCUSDT records=1000
2026-06-07T09:11:50Z | START request symbol=ETHUSDT interval=1h limit=1000
2026-06-07T09:11:56Z | END request symbol=ETHUSDT records=1000
2026-06-07T09:12:25Z | WROTE csv=data/clean/clean_market_data.csv records=10000
```

Example `results/runtime_comparison.csv`:

| method | seconds | records | note |
| --- | ---: | ---: | --- |
| serial | 105.1999 | 10000 | downloaded the ten symbols one after another |
| multithreading | 49.2628 | 10000 | downloaded several symbols at the same time |
