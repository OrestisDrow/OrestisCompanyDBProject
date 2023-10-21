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

# Make port 80 available to the world outside this container (Not used in this project)
EXPOSE 80

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/

# Make sure entrypoint is executable
RUN chmod +x /app/entrypoint.sh

# Use the entrypoint script as the default command
ENTRYPOINT ["/app/entrypoint.sh"]
