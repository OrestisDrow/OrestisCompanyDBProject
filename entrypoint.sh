#!/bin/bash

# Adjust permissions for the data directory
mkdir -p /app/data
chmod 777 /app/data

# Run the database initialization script
python /app/src/initialize_db.py

# Run the database population script
python /app/src/populate_db.py

# Run the custom script
exec python /app/src/my_script.py

chmod +x entrypoint.sh
