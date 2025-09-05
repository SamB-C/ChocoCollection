#!/bin/bash
# Run project inside its venv reliably

# Activate virtual environment
source "$(dirname "$0")/venv/bin/activate"

# Check first argument
case "$1" in
  input)
    shift  # remove "input" from args
    python "$(dirname "$0")/ChocoCollectionInput.py" "$@"
    ;;
  output)
    shift  # remove "output" from args
    python "$(dirname "$0")/ChocoCollectionOutput.py" "$@"
    ;;
  *)
    echo "Usage: $0 {input|output} [args...]"
    exit 1
    ;;
esac

