# Installation guide

1. Create a fork of this repo on your device.
2. Initialise a python virtual environment `python3 -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install dependencies `pip install -r requirements.txt`

# Running the program

Run `python3 ChocoCollectionInput.py` to input a new chocolate.
Run `python3 ChocoCollectionOutput.py` to output an existing chocolate.

To override narrations, provide the name of a narration file as an argument to `ChocoCollectionInput.py`, and read off the script in `Info.md`.
For example, to `python3 ChocoCollectionInput.py WelcomeInput`
