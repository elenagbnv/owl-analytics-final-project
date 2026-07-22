
# Details

Repository Link: https://github.com/elenagbnv/owl-analytics-final-project.git

Name: Elena Gubanova
---

## Project Team 1 purpose.

The purpise of Team 1 is Data Collection of market data from public API. Python script 'part1_build_dataset.py' extracts and downloads market data from Binance public market data  API and creates a log file 'api_download.log' where start and end time is recorder for each request, as well as how many records were received for each symbol, and when the final CSV is written.

---

## Before running the code.

To run the code, please use one of the options below depending on your operating system. Additionally, you will need Internet connection.

**Mac:**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

**Windows:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

> Optional: if activation is blocked, run a temporary PowerShell bypass (current session only):
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
> Then run: `.venv\Scripts\Activate.ps1`
> If activation is still blocked, run scripts directly with: `.venv\Scripts\python.exe your_script.py`

---

## How to run code for 'Team 1: Data Collection' and what it does.

Run the following python code in the terminal to create files: 1. 'clean_market_data.csv' file and 2.'api_download.log'
`python3 scripts/part1_build_dataset.py` 

---

## Location: 
- newly created 'clean_market_data.csv' file is saved in data/clean/ folder;
- newly created 'api_download.log' file is saved in results folder;

The 'part1_build_dataset.py 'script should create the data/clean/ and results/ folders automatically if they do not already exist.

---

## Output Expectations

1. 'clean_market_data.csv' file contains a mixed collection of market candles across 10 symbols and 1,000 timestamps per symbol.
- expected dataset size: 10,000 records
- 10 symbols
- 1,000 records per symbol
- 10,000 records total
- 1 header row in the CSV
- 10,001 lines total in data/clean/clean_market_data.csv

2. 'api_download.log' file contains entries with corresponding time stamps, indicating when each request starts, when each request finishes, how many records were received for each symbol, and when the final CSV is written.






