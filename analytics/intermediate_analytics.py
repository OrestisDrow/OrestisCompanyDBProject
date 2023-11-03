import sqlite3
import pandas as pd
import os
import sys

DATA_DIR = '/app/data/analytics/intermediate/'
DB_PATH = '/app/data/orestiscompanydb.sqlite'

def reformat_date(date_str):
    """
    Convert date string from YYYYMMDD format to YYYY-MM-DD format for queries
    Example Usage:
        start_date = reformat_date(sys.argv[1])
    """
    return "{}-{}-{}".format(date_str[:4], date_str[4:6], date_str[6:])

def customer_frequency(conn, start_date=None, end_date=None):
    query = """
    SELECT Customers.name, COUNT(DISTINCT DateInfo.date) AS purchase_frequency
    FROM Sales
    JOIN Customers ON Sales.customer_id = Customers.customer_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += """
    GROUP BY Customers.name
    ORDER BY purchase_frequency DESC, Customers.name
    """

    df = pd.read_sql_query(query, conn)
    return df

def avg_purchase_per_customer(conn, start_date=None, end_date=None):
    query = """
    SELECT Customers.name, AVG(Sales.quantity * Sales.unit_price) as avg_purchase_value
    FROM Sales
    JOIN Customers ON Sales.customer_id = Customers.customer_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Customers.name ORDER BY avg_purchase_value DESC"
    df = pd.read_sql_query(query, conn)
    return df

def sales_by_day_of_month(conn, start_date=None, end_date=None):
    query = """
    SELECT DateInfo.day, SUM(Sales.quantity * Sales.unit_price) as total_sales
    FROM Sales
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY DateInfo.day ORDER BY DateInfo.day ASC"
    df = pd.read_sql_query(query, conn)
    return df

def monthly_sales_trend(conn, start_date=None, end_date=None):
    query = """
    SELECT strftime('%Y-%m', DateInfo.date) as YearMonth, SUM(Sales.quantity * Sales.unit_price) as total_sales
    FROM Sales
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY YearMonth ORDER BY YearMonth ASC"
    df = pd.read_sql_query(query, conn)
    return df

def avg_sales_by_weekday(conn, start_date=None, end_date=None):
    query = """
    SELECT DateInfo.weekday, AVG(Sales.quantity * Sales.unit_price) AS avg_sales
    FROM Sales
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += """
    GROUP BY DateInfo.weekday
    ORDER BY
        CASE 
            WHEN DateInfo.weekday = 'Monday' THEN 1
            WHEN DateInfo.weekday = 'Tuesday' THEN 2
            WHEN DateInfo.weekday = 'Wednesday' THEN 3
            WHEN DateInfo.weekday = 'Thursday' THEN 4
            WHEN DateInfo.weekday = 'Friday' THEN 5
            WHEN DateInfo.weekday = 'Saturday' THEN 6
            WHEN DateInfo.weekday = 'Sunday' THEN 7
        END
    """
    df = pd.read_sql_query(query, conn)
    return df

def compute_intermediate_analytics(start_date=None, end_date=None):
    with sqlite3.connect(DB_PATH) as conn:
        avg_sales_by_weekday(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'avg_sales_by_weekday.csv'), index=False)
        sales_by_day_of_month(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'sales_by_day_of_month.csv'), index=False)
        monthly_sales_trend(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'monthly_sales_trend.csv'), index=False)
        customer_frequency(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'customer_frequency.csv'), index=False)
        avg_purchase_per_customer(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'avg_purchase_per_customer.csv'), index=False)
        
if __name__ == "__main__":
    # Make the data dir if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Check if the command-line args are provided
    if len(sys.argv) >= 3:
        start_date = reformat_date(sys.argv[1])
        end_date = reformat_date(sys.argv[2])
        compute_intermediate_analytics(start_date, end_date)
    else:
        print("Start date and end date arguments are required!")
        sys.exit(1)