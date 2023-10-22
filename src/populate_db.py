import sqlite3
import random
from datetime import date, timedelta

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
    for _ in range(2000):
        start_date = date(2021, 1, 1)
        end_date = date(2022, 12, 31)
        random_date = start_date + timedelta(days=random.randint(0, (end_date-start_date).days))
        random_date_id = cursor.execute('SELECT date_id FROM DateInfo WHERE date = ?', (random_date,)).fetchone()[0]
        random_store = random.randint(1, 5)
        random_product = random.randint(1, 10)
        random_customer = random.randint(1, 100)
        purchase_price = cursor.execute('SELECT purchase_price FROM Products WHERE product_id = ?', (random_product,)).fetchone()[0]
        sale_price = 1.1 * purchase_price
        quantity = random.randint(1, 10)
        cursor.execute('INSERT INTO Sales(date_id, store_id, product_id, customer_id, quantity, unit_price) VALUES (?, ?, ?, ?, ?, ?)', (random_date_id, random_store, random_product, random_customer, quantity, sale_price))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


if __name__ == "__main__":
    db_path = "/app/data/orestiscompanydb.sqlite"
    populate_database(db_path)
