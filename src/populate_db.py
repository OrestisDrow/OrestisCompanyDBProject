import sqlite3
import random

# Sample data for pseudo-random generation
STORE_LOCATIONS = ['London', 
                    'Paris', 
                    'Berlin', 
                    'Rome', 
                    'Madrid', 
                    'Lisbon', 
                    'Athens', 
                    'Warsaw']
PRODUCTS = [
    ('Samsung', 'Galaxy Note 10 Pro', 1000.0),
    ('Samsung', 'Galaxy S10', 800.0),
    ('Apple', 'iPhone X', 900.0),
    ('Apple', 'iPhone 11', 1100.0),
    # Add more products if desired
]
NAMES = ['John Doe',
        'Jane Smith',
        'Robert Brown',
        'Lucy White']  # Add more names if desired
EMAIL_DOMAINS = ['example.com', 'sample.net', 'demo.org']

def populate_database(db_path):
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Populate 'stores' table
    for location in STORE_LOCATIONS:
        cursor.execute('INSERT INTO stores (location) VALUES (?)', (location,))

    # Populate 'products' table
    for brand, name, price in PRODUCTS:
        cursor.execute('INSERT INTO products (brand, name, price) VALUES (?, ?, ?)', (brand, name, price))

    # Populate 'customers' table
    for name in NAMES:
        email = f"{name.split()[0].lower()}@{random.choice(EMAIL_DOMAINS)}"
        cursor.execute('INSERT INTO customers (name, email) VALUES (?, ?)', (name, email))

    # Populate 'transactions' table with pseudo-random data
    store_ids = [row[0] for row in cursor.execute('SELECT id FROM stores').fetchall()]
    product_ids = [row[0] for row in cursor.execute('SELECT id FROM products').fetchall()]
    customer_ids = [row[0] for row in cursor.execute('SELECT id FROM customers').fetchall()]
    
    for _ in range(100):  # Inserting 100 transactions
        cursor.execute('''
            INSERT INTO transactions (store_id, product_id, customer_id, date)
            VALUES (?, ?, ?, ?)
        ''', (
            random.choice(store_ids),
            random.choice(product_ids),
            random.choice(customer_ids),
            f"2023-{random.randint(1, 12)}-{random.randint(1, 28)}"  # Random date in 2023
        ))

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_path = "app/data/orestiscompanydb.sqlite"
    populate_database(db_path)
