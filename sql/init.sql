/*
    Orestis Company Database Schema

    This database schema is designed to support analytics for Orestis Company's sales data. 
    The structure follows a star schema pattern, optimized for querying large data sets and 
    suitable for OLAP (Online Analytical Processing) systems.

    - `stores`: Dimension table that holds information about the different store locations.
    - `products`: Dimension table capturing the product details, including the purchase price from suppliers.
    - `customers`: Dimension table containing customer information.
    - `date_info`: Dimension table designed to support date-based analytics. Contains various date attributes to facilitate time-based querying.
    - `sales`: Fact table that logs each sale, capturing the sale price, the product, customer, store, and the date of the transaction.

    The schema is designed to be extensible. As business needs evolve, additional dimensions or measures can be easily integrated.

    Notes:
        - I could also put a regex constraint for the email format, but since SQLite doesn't natively
          support regex-based constraints, and since the purposes of this project is for showcasing
          only, I would like to keep the complexity minimal.
        - For the same reason as above, I am only putting constraint in DateInfo.day to be between
          1 and 31 even though February can have up to 28.
*/

-- Stores dimension
CREATE TABLE IF NOT EXISTS Stores (
    store_id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    street_number TEXT NOT NULL,
    city TEXT NOT NULL,
    state TEXT,
    postal_code TEXT NOT NULL,
    country TEXT NOT NULL
);

-- Products dimension
CREATE TABLE IF NOT EXISTS Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    brand TEXT NOT NULL,
    purchase_price REAL NOT NULL CHECK (purchase_price >= 0)  -- Price that the company aquired the product
);

-- Customers dimension
CREATE TABLE IF NOT EXISTS Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL
);

-- Date dimension
CREATE TABLE IF NOT EXISTS DateInfo (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE CHECK (date <= CURRENT_DATE),  -- ensuring no future dates
    year INTEGER CHECK (year BETWEEN 2000 AND 2100),
    month INTEGER CHECK (month BETWEEN 1 AND 12),
    day INTEGER CHECK (day BETWEEN 1 AND 31),
    weekday TEXT CHECK (weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'))
);

-- Sales fact table
CREATE TABLE IF NOT EXISTS Sales (
    sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
    date_id INTEGER,
    store_id INTEGER,
    product_id INTEGER,
    customer_id INTEGER,
    quantity INTEGER NOT NULL CHECK (quantity > 0),     -- positive quantity for products sold
    unit_price REAL NOT NULL CHECK (unit_price >= 0),   -- non-negative prices
    FOREIGN KEY (date_id) REFERENCES DateInfo(date_id),
    FOREIGN KEY (store_id) REFERENCES Stores(store_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

-- Indexing foreign keys in the fact table
CREATE INDEX IF NOT EXISTS idx_sales_date ON Sales(date_id);
CREATE INDEX IF NOT EXISTS idx_sales_store ON Sales(store_id);
CREATE INDEX IF NOT EXISTS idx_sales_product ON Sales(product_id);
CREATE INDEX IF NOT EXISTS idx_sales_customer ON Sales(customer_id);

-- Indexing the date in the date dimension since it is going to be joined frequently in analytics
CREATE INDEX IF NOT EXISTS idx_date_info_date ON DateInfo(date);

