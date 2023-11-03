#!/bin/sh
set -e

# Run the python script that pre-computes and stores intermediate analytics 
python3 /app/analytics/intermediate_analytics.py $1 $2