from flask import Flask, render_template, request, redirect, url_for, Response
import pandas as pd
import os
import time
import subprocess

app = Flask(__name__)

# Define paths to CSV files for each category
CSV_FILES = {
    "NIFTY-500_TOP_STOCKS": r'D:/stockmarket projects/Screener/data/NIFTY-500_TOP_STOCKS.csv',
    "NIFTY-COMMODITIES": r'D:/stockmarket projects/Screener/data/NIFTY-COMMODITIES.csv',
    "NIFTY-CONSUMPTION": r'D:/stockmarket projects/Screener/data/NIFTY-CONSUMPTION.csv',
    "NIFTY-DIGITAL": r'D:/stockmarket projects/Screener/data/NIFTY-DIGITAL.csv',
    "NIFTY-DIVIDEND-OPPORTUNITIES": r'D:/stockmarket projects/Screener/data/NIFTY-DIVIDEND-OPPORTUNITIES.csv',
    "NIFTY-INFRASTRUCTURE": r'D:/stockmarket projects/Screener/data/NIFTY-INFRASTRUCTURE.csv',
    "NIFTY-MANUFACTURING": r'D:/stockmarket projects/Screener/data/NIFTY-MANUFACTURING.csv',
    "NIFTY-MICROCAP-250": r'D:/stockmarket projects/Screener/data/NIFTY-MICROCAP-250.csv',
    "NIFTY-MIDSMALLCAP": r'D:/stockmarket projects/Screener/data/NIFTY-MIDSMALLCAP.csv',
    "NIFTY-OIL-&-GAS": r'D:/stockmarket projects/Screener/data/NIFTY-OIL-&-GAS.csv',
    "NIFTY-TATA-GROUP": r'D:/stockmarket projects/Screener/data/NIFTY-TATA-GROUP.csv',
}

def clean_column_names(df):
    # Strip whitespace from column names
    df.columns = df.columns.str.strip()
    return df

def rounding_bottom_check(stock_data):
    # Placeholder logic for rounding bottom check
    return True

@app.route('/')
def index():
    # Display the category buttons
    return render_template('index.html', categories=CSV_FILES.keys())

@app.route('/process', methods=['POST'])
def process():
    # Get the selected category
    category = request.form['category']
    if category not in CSV_FILES:
        return redirect(url_for('index'))

    # Call FetchStockData.py to update stock data
    subprocess.call(["python", "FetchStockData.py"])

    # Redirect to progress page with the selected category
    return redirect(url_for('progress', category=category))

@app.route('/progress/<category>')
def progress(category):
    return render_template('progress.html', category=category)

@app.route('/progress_stream/<category>')
def progress_stream(category):
    def generate():
        # Load CSV for the selected category
        file_path = CSV_FILES.get(category)
        if not file_path:
            yield f"data: 100,Error loading CSV for {category}\n\n"
            return

        # Load and clean stock data
        df = pd.read_csv(file_path)
        df = clean_column_names(df)
        stock_symbols = df['SYMBOL'].tolist()
        total_stocks = len(stock_symbols)

        for idx, symbol in enumerate(stock_symbols):
            time.sleep(0.1)  # Simulate processing time
            progress = (idx + 1) / total_stocks * 100

            # Check if stock meets rounding bottom criteria
            stock_file_path = os.path.join('D:/stockmarket projects/Screener/data/stock_data', f"{symbol}.csv")
            if os.path.exists(stock_file_path):
                stock_data = pd.read_csv(stock_file_path)
                if rounding_bottom_check(stock_data):
                    yield f"data: {progress:.2f},{symbol}\n\n"
                else:
                    yield f"data: {progress:.2f},\n\n"
            else:
                yield f"data: {progress:.2f},\n\n"
            
    return Response(generate(), mimetype='text/event-stream')

if __name__ == "__main__":
    app.run(debug=True)
