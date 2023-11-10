import sqlite3
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import os
import sys
from datetime import datetime

DATA_DIR = '/app/data/analytics/advanced/'
DB_PATH = '/app/data/orestiscompanydb.sqlite'

def reformat_date(date_str):
    """
    Convert date string from YYYYMMDD format to YYYY-MM-DD format for SQLLite queries
    Example Usage:
        start_date = reformat_date(sys.argv[1])
    """
    return "{}-{}-{}".format(date_str[:4], date_str[4:6], date_str[6:])

def calculate_daily_profits(conn, start_date=None, end_date=None):
    query = """
    SELECT DateInfo.date, 
           SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) as daily_profit
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    
    query += "GROUP BY DateInfo.date ORDER BY DateInfo.date ASC"
    
    df = pd.read_sql(query, conn)
    return df

def compute_bollinger_bands(daily_profits_df, window_size=20, num_std_dev=2):

    # Need more than 3 times the window size for bollinger bands to be reliable
    if len(daily_profits_df) < window_size*3:
        return None


    # Calculate moving average
    daily_profits_df['moving_avg'] = daily_profits_df['daily_profit'].rolling(window=window_size).mean()
    # Calculate moving standard deviation
    daily_profits_df['moving_std_dev'] = daily_profits_df['daily_profit'].rolling(window=window_size).std()
    # Calculate upper Bollinger Bands
    daily_profits_df['upper_band'] = daily_profits_df['moving_avg'] + (daily_profits_df['moving_std_dev']*num_std_dev)
    # Calculate lower Bollinger Bands
    daily_profits_df['lower_band'] = daily_profits_df['moving_avg'] - (daily_profits_df['moving_std_dev']*num_std_dev)
    
    # Select only required columns
    bollinger_bands_df = daily_profits_df[['date', 'daily_profit', 'lower_band', 'moving_avg', 'upper_band']]
    bollinger_bands_df.columns = ['date', 'daily_profit', 'lower_band', 'moving_avg', 'upper_band']
    return bollinger_bands_df

def calculate_product_profit_margin(conn, start_date=None, end_date=None):
    query = """
    SELECT Products.product_id,
           Products.name,
           AVG(Sales.unit_price - Products.purchase_price) / AVG(Sales.unit_price) as profit_margin
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += "GROUP BY Products.product_id, Products.name ORDER BY profit_margin DESC"
    
    df = pd.read_sql(query, conn)
    return df[['name', 'profit_margin']]

def calculate_store_profit_margin(conn, start_date=None, end_date=None):
    query = """
    SELECT Stores.store_id,
           Stores.city,
           SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) AS total_profit,
           SUM(Sales.unit_price * Sales.quantity) AS total_sales,
           (SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) / SUM(Sales.unit_price * Sales.quantity)) AS profit_margin
    FROM Sales
    JOIN Stores ON Sales.store_id = Stores.store_id
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += "GROUP BY Stores.store_id, Stores.city ORDER BY profit_margin DESC"
    df = pd.read_sql(query, conn)
    return df[['store_id', 'city', 'profit_margin']]

def forecast_with_arima(series, order, steps=5):
    # Check if the series index has a frequency set; if not, attempt to infer it
    if series.index.freq is None:
        # Assuming the series should have a daily frequency
        series = series.asfreq('D')

    # Fit the ARIMA model
    model = ARIMA(series, order=order)
    model_fit = model.fit()
    
    # Forecast 'steps' ahead
    forecast = model_fit.forecast(steps=steps)
    return forecast


def forecast_daily_profits(conn, start_date=None, end_date=None, forecast_steps=5):
    # First, calculate daily profits
    daily_profits_df = calculate_daily_profits(conn, start_date, end_date)
    historical_profits_df = daily_profits_df.copy(deep=True)

    # Ensure that the 'date' column is a datetime type and set as index
    daily_profits_df['date'] = pd.to_datetime(daily_profits_df['date'])
    daily_profits_df.set_index('date', inplace=True)

    # ARIMA Model order (p,d,q) can be determined using ACF and PACF plots or grid search methods
    order = (1, 1, 1)
    
    # We need at least 60 days of data to forecast 5 days ahead
    if len(daily_profits_df) < 60:
        return None

    forecasted_profits = forecast_with_arima(daily_profits_df['daily_profit'], order, steps=forecast_steps)
    forecasted_profits = forecasted_profits.reset_index()
    
    # Rename the columns to give them appropriate names
    forecasted_profits.columns = ['date', 'daily_profit']
    
    # Convert the 'date' column to datetime type and extract only the date
    forecasted_profits['date'] = forecasted_profits['date'].dt.date

    # Combine the original daily profits with the forecasted profits
    combined_df = pd.concat([historical_profits_df, forecasted_profits], ignore_index=True)
        
    return combined_df[['date', 'daily_profit']]


def calculate_rfm_scores(conn, start_date=None, end_date=None):

    # Need at least 60 days of data to reliably calculate RFM scores
    if (datetime.strptime(end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')).days < 60:
        return None
    # Set current_date as end_date if provided, otherwise default to '20221231'
    current_date = end_date if end_date else '20221231'
    
    # Format current_date for SQL query
    formatted_current_date = current_date
    
    query = """
    SELECT
        Customers.customer_id,
        Customers.name,
        MAX(DateInfo.date) as last_purchase_date,
        COUNT(DISTINCT Sales.sale_id) as frequency,
        SUM(Sales.quantity * Sales.unit_price) as monetary
    FROM Sales
    JOIN Customers ON Sales.customer_id = Customers.customer_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """

    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{formatted_current_date}'"
    
    query += " GROUP BY Customers.customer_id, Customers.name"

    rfm_df = pd.read_sql(query, conn)
    
    # Calculate Recency as days since last purchase
    rfm_df['recency'] = (pd.to_datetime(formatted_current_date) - pd.to_datetime(rfm_df['last_purchase_date'])).dt.days
    
    # Assign RFM scores from 1 to 5
    rfm_df['r_score'] = pd.qcut(rfm_df['recency'], 5, labels=[5, 4, 3, 2, 1], duplicates='drop') # Note that a lower 'recency' is better
    rfm_df['f_score'] = pd.qcut(rfm_df['frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5], duplicates='drop')
    rfm_df['m_score'] = pd.qcut(rfm_df['monetary'], 5, labels=[1, 2, 3, 4, 5], duplicates='drop')

    # Combine RFM scores into a single RFM segment code and RFM score
    rfm_df['rfm_segment'] = rfm_df['r_score'].astype(str) + rfm_df['f_score'].astype(str) + rfm_df['m_score'].astype(str)
    rfm_df['rfm_score'] = rfm_df['r_score'].astype(int) + rfm_df['f_score'].astype(int) + rfm_df['m_score'].astype(int)
    
    # Select only the necessary columns to save to CSV
    rfm_scores_df = rfm_df[['customer_id', 'r_score', 'f_score', 'm_score', 'rfm_segment', 'rfm_score']]
    
    return rfm_scores_df


def compute_advanced_analytics(start_date=None, end_date=None):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            # Calculate daily profits, compute bollinger bands and save to csv
            daily_profits_df = calculate_daily_profits(conn, start_date, end_date)
            bollinger_bands_df = compute_bollinger_bands(daily_profits_df)
            if bollinger_bands_df is not None:
                bollinger_bands_df.to_csv(os.path.join(DATA_DIR, 'daily_profits_bollinger_bands.csv'), index=False)

            # Calculate product profit margins and save to csv
            product_profit_margin_df = calculate_product_profit_margin(conn, start_date, end_date)
            product_profit_margin_df.to_csv(os.path.join(DATA_DIR, 'product_profit_margins.csv'), index=False)

            # Calculate store profit margins and save to csv
            store_profit_margin_df = calculate_store_profit_margin(conn, start_date, end_date)
            store_profit_margin_df.to_csv(os.path.join(DATA_DIR, 'store_profit_margins.csv'), index=False)

            # Forecast daily profits and save to csv
            forecasted_profits = forecast_daily_profits(conn, start_date, end_date, 5)
            if forecasted_profits is not None:
                forecasted_profits.to_csv(os.path.join(DATA_DIR, 'profit_forecast.csv'), index=False)

            # Calculate RFM scores and save to CSV
            rfm_scores_df = calculate_rfm_scores(conn, start_date, end_date)
            if rfm_scores_df is not None:
                rfm_scores_df.to_csv(os.path.join(DATA_DIR, 'rfm_scores.csv'), index=False)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        sys.exit(1)
        
if __name__ == "__main__":
    # Make the data dir if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Check if the command-line args are provided
    if len(sys.argv) >= 3:
        start_date = reformat_date(sys.argv[1])
        end_date = reformat_date(sys.argv[2])
        compute_advanced_analytics(start_date, end_date)
    else:
        print("Start date and end date arguments are required!")
        sys.exit(1)