#!/bin/bash
set -e

# Run the SQL script that sets up the database schema
sqlite3 /app/data/orestiscompanydb.sqlite < /app/sql/init.sql
