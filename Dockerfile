# Use an official Python runtime as the parent image
FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install SQLite
RUN apt-get update && apt-get install -y sqlite3 && apt-get clean

# Adjust permissions for the data directory
RUN mkdir -p /app/data && \
    chmod 777 /app/data

# Go directly into the provided user-friendly CLI unless user bypasses the entrypoint
COPY entrypoint.sh /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []