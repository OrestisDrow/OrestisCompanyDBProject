#!/bin/bash

# If no arguments are provided, default to starting the CLI.
if [ "$#" -eq 0 ]; then
    exec python /app/src/cli.py repl
else
    # Otherwise, execute the passed command.
    exec "$@"
fi
