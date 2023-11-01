#!/bin/sh
set -e

# Run the python script that pre-computes and stores basic analytics 
python3 /app/analytics/basic_analytics.py $1 $2
