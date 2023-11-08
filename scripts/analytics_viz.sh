#!/bin/bash

# Add the parent directory of `analytics_dashboard` to PYTHONPATH
export PYTHONPATH="/app:$PYTHONPATH"

python3 -m analytics_dashboard.app

