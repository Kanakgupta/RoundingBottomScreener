import yfinance as yf
import os
import pandas as pd
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

# Define the paths
CSV_FILE_PATH = r'D:\stockmarket projects\Screener\data\nse_stocks_all.csv'
DATA_FOLDER = r'D:\stockmarket projects\Screener\data\stock_data'
DATE_FORMAT = "%Y-%m-%d"
last_modified_time = None

def is_data_outdated(file_path):
    """Check if the stock data needs to be updated (older than 1 day)."""
    if not os.path.exists(file_path):
        return True

    # Get the last modified time of the file
    last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
    current_time = datetime.now()

    # If the file is older than 1 day, consider it outdated
    return current_time - last_modified_time > timedelta(days=1)

def download_stock_data(symbol, start_date='2005-01-01', end_date=None):
    """Downloads or loads historical data for a stock symbol from yfinance."""
    # Create the data folder if it doesn't exist
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    
    # Filepath where data will be stored
    file_path = os.path.join(DATA_FOLDER, f"{symbol}.csv")
    
    # If the data is outdated or the file doesn't exist, fetch new data
    if is_data_outdated(file_path):
        print(f"Downloading updated data for {symbol} from Yahoo Finance...")
        df = yf.download(f'{symbol}.NS', start=start_date, end=end_date)
        
        # Save the data to a CSV file for future use
        if not df.empty:
            df.to_csv(file_path)
            print(f"Data saved to {file_path}")
            return df
        else:
            print(f"No data found for {symbol}")
            return None
    else:
        print(f"Loading data from {file_path}")
        return pd.read_csv(file_path, index_col='Date', parse_dates=True)

def get_stock_symbols(csv_file_path):
    df = pd.read_csv(csv_file_path)
    print(df.columns)  # Print the columns to debug
    df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
    symbols = df['SYMBOL'].tolist()  # Access the 'SYMBOL' column
    return symbols


def update_stock_data():
    """Fetches stock data for all symbols in the CSV."""
    print("Starting stock data update...")
    symbols = get_stock_symbols(CSV_FILE_PATH)
    
    if not symbols:
        print("No symbols found in the CSV file.")
        return
    
    end_date = datetime.today().strftime(DATE_FORMAT)
    start_date = (datetime.today().replace(year=datetime.today().year - 12)).strftime(DATE_FORMAT)

    # Fetch stock data for each symbol
    for symbol in symbols:
        print(f"Processing {symbol}...")
        download_stock_data(symbol, start_date, end_date)
    print("Stock data update completed.")

def check_csv_modification():
    """Check if the CSV file has been modified and trigger stock data update."""
    global last_modified_time
    try:
        modified_time = os.path.getmtime(CSV_FILE_PATH)
        if last_modified_time is None or modified_time != last_modified_time:
            print("CSV file has been modified. Updating stock data...")
            last_modified_time = modified_time
            update_stock_data()
        else:
            print("No changes detected in the CSV file.")
    except Exception as e:
        print(f"Error checking CSV modification: {e}")

def run_initial_stock_update():
    """Run an immediate update if the script is executed, download all missing data."""
    print("Running initial stock update check...")
    update_stock_data()

# Schedule the task to run at 4 PM PST or if CSV is modified
scheduler = BlockingScheduler()

# Schedule daily update at 4 PM PST (16:00 PST)
scheduler.add_job(check_csv_modification, 'cron', hour=16, minute=0, timezone='US/Pacific')
print("Scheduler started, checking stock data at 4 PM PST.")

# Run an initial update on script start
run_initial_stock_update()

# Start the scheduler
scheduler.start()
