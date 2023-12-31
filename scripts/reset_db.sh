#!/bin/bash

# Adjust permissions for the data directory
mkdir -p /app/data
chmod 777 /app/data

# Remove the existing database file
rm -f /app/data/orestiscompanydb.sqlite

# Initialize the database using init.sql
sqlite3 /app/data/orestiscompanydb.sqlite < /app/sql/init.sql

# Run the database population script
python /app/src/populate_db.py
