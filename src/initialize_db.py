import sqlite3

def setup_database(db_path):
    # Connect to the SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create the 'stores' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT NOT NULL
        );
    ''')

    # Create the 'products' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brand TEXT NOT NULL,
            price REAL NOT NULL
        );
    ''')

    # Create the 'customers' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL
        );
    ''')

    # Create the 'transactions' table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER,
            product_id INTEGER,
            customer_id INTEGER,
            date TEXT NOT NULL,
            FOREIGN KEY (store_id) REFERENCES stores (id),
            FOREIGN KEY (product_id) REFERENCES products (id),
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        );
    ''')

    # Commit the changes and close the connection
    connection.commit()
    connection.close()

if __name__ == "__main__":
    db_path = "app/data/orestiscompanydb.sqlite"
    setup_database(db_path)
