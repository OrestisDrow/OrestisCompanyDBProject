# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# Copy only the requirements.txt first to benefit from Docker's caching
# Unless requirements.txt changes, the time consuming pip install won't be rerun
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Adjust permissions for the data directory
RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Go directly into the provided user-friendly CLI unless user bypasses the entrypoint
COPY entrypoint.sh /app/entrypoint.sh

# Give entrypoint execution permissions
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD []