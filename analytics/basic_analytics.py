import sqlite3
import pandas as pd
import os
import sys
from datetime import datetime

DATA_DIR = '/app/data/analytics/basic/'
DB_PATH = '/app/data/orestiscompanydb.sqlite'

def reformat_date(date_str):
    """
    Convert date string from YYYYMMDD format to YYYY-MM-DD format for queries
    Example Usage:
        start_date = reformat_date(sys.argv[1])
    """
    return "{}-{}-{}".format(date_str[:4], date_str[4:6], date_str[6:])

def total_sales(conn, start_date=None, end_date=None):
    query = """
    SELECT SUM(Sales.quantity * Sales.unit_price) as total_sales
    FROM Sales
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    df = pd.read_sql(query, conn)
    return df["total_sales"]


def sales_by_product(conn, start_date=None, end_date=None):
    query = """
    SELECT Products.name, SUM(Sales.quantity * Sales.unit_price) as sales_by_product
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Products.name"
    df = pd.read_sql(query, conn)
    return df


def sales_by_region(conn, start_date=None, end_date=None):
    query = """
    SELECT Stores.city, SUM(Sales.quantity * Sales.unit_price) as sales_by_region
    FROM Sales
    JOIN Stores ON Sales.store_id = Stores.store_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Stores.city"
    df = pd.read_sql(query, conn)
    return df

def profit_total(conn, start_date=None, end_date=None):
    query = """
    SELECT SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) as total_profit
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    df = pd.read_sql(query, conn)
    return df["total_profit"]

def profit_by_product(conn, start_date=None, end_date=None):
    query = """
    SELECT Products.name, SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) as profit_by_product
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Products.name"
    df = pd.read_sql(query, conn)
    return df

def profit_by_region(conn, start_date=None, end_date=None):
    query = """
    SELECT Stores.city, SUM((Sales.unit_price - Products.purchase_price) * Sales.quantity) as profit_by_region
    FROM Sales
    JOIN Stores ON Sales.store_id = Stores.store_id
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Stores.city"
    df = pd.read_sql(query, conn)
    return df

def top_selling_products(conn, start_date=None, end_date=None, limit=3):
    query = """
    SELECT Products.name, SUM(Sales.quantity * Sales.unit_price) as total_sales
    FROM Sales
    JOIN Products ON Sales.product_id = Products.product_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Products.name ORDER BY total_sales DESC LIMIT ?"
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df

def top_customers(conn, start_date=None, end_date=None, limit=3):
    query = """
    SELECT Customers.name, SUM(Sales.quantity * Sales.unit_price) as total_spent
    FROM Sales
    JOIN Customers ON Sales.customer_id = Customers.customer_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY Customers.name ORDER BY total_spent DESC LIMIT ?"
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df

def top_stores_by_sales(conn, start_date=None, end_date=None, limit=3):
    query = """
    SELECT Stores.address || ', ' || Stores.city as store_location, SUM(Sales.quantity * Sales.unit_price) as total_sales
    FROM Sales
    JOIN Stores ON Sales.store_id = Stores.store_id
    JOIN DateInfo ON Sales.date_id = DateInfo.date_id
    """
    if start_date and end_date:
        query += f" WHERE DateInfo.date BETWEEN '{start_date}' AND '{end_date}'"
    query += " GROUP BY store_location ORDER BY total_sales DESC LIMIT ?"
    df = pd.read_sql_query(query, conn, params=(limit,))
    return df


def compute_basic_analytics(start_date=None, end_date=None):
    with sqlite3.connect(DB_PATH) as conn:
        total_sales(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'total_sales.csv'), index=False)
        sales_by_product(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'sales_by_product.csv'), index=False)
        sales_by_region(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'sales_by_region.csv'), index=False)
        profit_total(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'profit_total.csv'), index=False)
        profit_by_product(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'profit_by_product.csv'), index=False)
        profit_by_region(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'profit_by_region.csv'), index=False)
        top_selling_products(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'top_selling_products.csv'), index=False)
        top_customers(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'top_customers.csv'), index=False)
        top_stores_by_sales(conn, start_date, end_date).to_csv(os.path.join(DATA_DIR, 'top_stores_by_sales.csv'), index=False)

if __name__ == "__main__":
    # Make the data dir if not exists
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Check if the command-line args are provided
    if len(sys.argv) >= 3:
        start_date = reformat_date(sys.argv[1])
        end_date = reformat_date(sys.argv[2])
        compute_basic_analytics(start_date, end_date)
    else:
        print("Start date and end date arguments are required!")
        sys.exit(1)