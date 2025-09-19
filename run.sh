#!/bin/bash
# Run project inside its venv reliably

# Activate virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Check first argument
case "$1" in
  input)
    shift  # remove "input" from args
    python3 "$(dirname "$0")/ChocoCollectionInput.py" "$@"
    ;;
  output)
    shift  # remove "output" from args
    python3 "$(dirname "$0")/ChocoCollectionOutput.py" "$@"
    ;;
  record)
    shift  # remove "record" from args
    python3 "$(dirname "$0")/record.py" "$@"
    ;;
  *)
    echo "Usage: $0 {input|output|record} [args...]"
    exit 1
    ;;
esac

