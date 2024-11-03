import pandas as pd
import os
import yfinance as yf

def is_rounding_bottom(stock_data):
    """
    Check if the provided stock data meets the criteria for a rounding bottom.
    This function expects a DataFrame with stock price data.
    """
    if isinstance(stock_data, pd.DataFrame) and not stock_data.empty:
        # Assuming 'Close' column exists in stock_data
        all_time_low = stock_data['Close'].min()
        current_price = stock_data['Close'].iloc[-1]  # Get the latest price
        
        if current_price > 1.2 * all_time_low and current_price < 1.4 * all_time_low:
            return True
    return False

def scan_and_update_stocks(stock_symbols, stock_data_dir):
    """
    Scan for all stocks in the stock_data_dir, checking for rounding bottom patterns
    and updating the stock data as necessary.
    """
    rounding_bottom_stocks = []

    for symbol in stock_symbols:
        stock_file_path = os.path.join(stock_data_dir, f"{symbol}.csv")
        if os.path.exists(stock_file_path):
            stock_data = pd.read_csv(stock_file_path)
            if is_rounding_bottom(stock_data):
                rounding_bottom_stocks.append(symbol)

    return rounding_bottom_stocks

if __name__ == "__main__":
    # Define the directory where stock data is stored
    stock_data_dir = 'D:/stockmarket projects/Screener/data/stock_data'
    
    # Load all stock symbols from a specified CSV file (adjust the path as necessary)
    # For this example, let's assume a file containing all symbols
    all_stock_symbols_path = 'D:/stockmarket projects/Screener/data/NIFTY-500_TOP_STOCKS.csv'  # Change this if needed
    all_stock_symbols_df = pd.read_csv(all_stock_symbols_path)
    all_stock_symbols = all_stock_symbols_df['SYMBOL'].tolist()  # Adjust column name as needed
    
    # Call the scan_and_update_stocks function
    rounding_bottom_stocks = scan_and_update_stocks(all_stock_symbols, stock_data_dir)

    # Print or log the results
    print("Rounding Bottom Stocks:", rounding_bottom_stocks)
