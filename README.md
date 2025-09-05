# Installation guide

1. Create a fork of this repo on your device.
2. Initialise a python virtual environment `python3 -m venv venv`
3. Activate the virtual environment `source venv/bin/activate`
4. Install dependencies `pip install -r requirements.txt`

# Running the program

Run `./run.sh input` to input a new chocolate.
Run `./run.sh output` to output an existing chocolate.

To override narrations, provide the name of a narration file as an argument to `./run.sh input`, and read off the script in `Info.md`.
For example, to `./run.sh input WelcomeInput`
