"""
This script, populate_db.py, is designed to populate the SQLite database for the OrestisCompany analytics application. 
It performs the following tasks:

1. Populate Stores: 
    Inserts predefined data for various store locations, including address details and geographic information.

2. Populate Products: 
    Inserts a range of products with details like name, brand, and purchase price. Includes popular electronics like iPhones, Samsung Galaxy series, and Huawei models.

3. Populate Customers: 
    Generates and inserts data for 100 customers, including their names and email addresses.

4. Populate DateInfo: 
    Generates and inserts date information for the years 2021 and 2022. Each date entry includes the date, year, month, day, and weekday.

5. Populate Sales: Creates and inserts sales data with a mix of deterministic and probabilistic approaches. This includes:
   - Randomly selecting a subset of stores and products to be considered high revenue and high margin, respectively.
   - Generating sales records for a 2-year period (2021-2022) with random dates, customers, stores, and products.
   - Applying different distribution strategies for sales quantity and pricing, considering high-margin products and high-revenue stores.

The script uses the sqlite3 module to interact with the SQLite database and employs the random and datetime modules to generate varied and realistic data. 
It's a crucial part of the setup process for the OrestisCompany analytics application, ensuring that the database is rich with diverse and representative data for analysis.
"""

import sqlite3
import random
from datetime import date, timedelta
import math

def populate_database(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Populate Stores
    stores_data = [
        ('1 High Street', '100', 'London', 'Greater London', 'W1 1AA', 'UK'),
        ('2 Main Street', '200', 'Paris', 'Île-de-France', '75001', 'France'),
        ('3 Via Roma', '300', 'Rome', 'Lazio', '00184', 'Italy'),
        ('4 Markt', '400', 'Berlin', 'Berlin', '10178', 'Germany'),
        ('5 Plaza Mayor', '500', 'Madrid', 'Community of Madrid', '28012', 'Spain')
    ]
    cursor.executemany('INSERT INTO Stores(address, street_number, city, state, postal_code, country) VALUES (?, ?, ?, ?, ?, ?)', stores_data)

    # 2. Populate Products
    products_data = [
        ('iPhone 13', 'Apple', 699.99),
        ('iPhone 13 Pro', 'Apple', 999.99),
        ('iPhone 13 Mini', 'Apple', 599.99),
        ('Galaxy S22', 'Samsung', 799.99),
        ('Galaxy S22 Ultra', 'Samsung', 1199.99),
        ('Galaxy S22 Plus', 'Samsung', 999.99),
        ('Galaxy A12', 'Samsung', 179.99),
        ('Galaxy A52', 'Samsung', 349.99),
        ('P50', 'Huawei', 599.99),
        ('P50 Pro', 'Huawei', 899.99)
    ]
    cursor.executemany('INSERT INTO Products(name, brand, purchase_price) VALUES (?, ?, ?)', products_data)

    # 3. Populate Customers
    customers_data = [('Customer'+str(i), 'customer'+str(i)+'@gmail.com') for i in range(1, 101)]
    cursor.executemany('INSERT INTO Customers(name, email) VALUES (?, ?)', customers_data)

    # 4. Populate DateInfo
    dates_data = []
    for y in [2021, 2022]:    # Assume years 2021 and 2022 to fulfull thhe date constraint
        for i in range(365):  # Assuming non-leap years for simplicity
            current_date = date(y, 1, 1) + timedelta(days=i)
            dates_data.append(
                (current_date, 
                current_date.year, 
                current_date.month, 
                current_date.day, 
                current_date.strftime('%A'))
            )
    cursor.executemany('INSERT INTO DateInfo(date, year, month, day, weekday) VALUES (?, ?, ?, ?, ?)', dates_data)

    # 5. Populate Sales
    # Randomly select 20% of stores as high margin/revenew stores
    high_revenue_stores = random.sample(range(1, 6), 5 // 5)
    # Randomly select 20% of products as high margin products
    high_margin_products = random.sample(range(1, 11), 3)  # Assume product IDs range from 1 to 10
    for _ in range(2000):
        start_date = date(2021, 1, 1)
        end_date = date(2022, 12, 31)

        # Dates will follow uniform distribution
        random_date = start_date + timedelta(days=random.randint(0, (end_date-start_date).days))
        random_date_id = cursor.execute('SELECT date_id FROM DateInfo WHERE date = ?', (random_date,)).fetchone()[0]
        
        # Gaussian distribution for customers
        random_customer = int(max(1, min(100, math.ceil(random.gauss(50, 15)))))
        
        # Skewed distribution for store (higher chance for high revenue stores)
        if random.random() < 0.8:  # 80% chance to pick a high revenue store
            random_store = random.choice(high_revenue_stores)
        else:
            random_store = random.randint(1, 5)

        # Skewed distribution for product (higher chance for certain products)
        if random.random() < 0.8:  # 80% chance to pick a high volume product
            random_product = random.choice(high_margin_products)
        else:
            random_product = random.randint(1, 10)

        purchase_price = cursor.execute('SELECT purchase_price FROM Products WHERE product_id = ?', (random_product,)).fetchone()[0]
        
         # Adjust sale_price_multiplier based on product
        if random_product in high_margin_products:
            sale_price_multiplier = max(1.5, min(2, random.gauss(1.75, 0.15)))
        else:
            sale_price_multiplier = max(1.1, min(1.5, random.gauss(1.25, 0.1)))
        
        sale_price = purchase_price * sale_price_multiplier

        # Skewed distribution for quantity based on both high-margin products and high-revenue stores
        if random_store in high_revenue_stores or random_product in high_margin_products:
            quantity = int(max(1, min(10, math.ceil(random.gauss(7, 1.5)))))
        else:
            quantity = int(max(1, min(10, math.ceil(random.gauss(3, 1)))))
        
        cursor.execute('INSERT INTO Sales(date_id, store_id, product_id, customer_id, quantity, unit_price) VALUES (?, ?, ?, ?, ?, ?)', (random_date_id, random_store, random_product, random_customer, quantity, sale_price))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_path = "/app/data/orestiscompanydb.sqlite"
    populate_database(db_path)
