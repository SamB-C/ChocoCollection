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

## Fun ways to run the program  
For MacOS, use Automator.app

1. Open Automator
   - Press Cmd + Space → type Automator → hit Enter.
2. Create a new application
   - Choose New Document → select Application.
3. Add a “Run Shell Script” action
   - In the left panel, search for “Run Shell Script”.
   - Drag it into the workflow area.
4. Inside it, paste:

```bash
# For the input script
osascript -e 'tell application "Terminal"
    do script "cd \"/Fixed/path/to/directory\" && ./run.sh input"
end tell'
```

```bash
# For the output script
osascript -e 'tell application "Terminal"
    do script "cd \"/Fixed/path/to/directory\" && ./run.sh output"
end tell'
```

    - Where `Fixed/path/to/directory` is the path to your installation of the depository.

5. Save it
   - Save as ChocoInput.app (or whatever name you like).
   - Choose Application as the location, so you can then put it in the dock
6. Make it executable
   - Sometimes Automator apps don’t have execute permissions. Run this in terminal: `chmod +x ~/Desktop/ChocoInput.app`
7. Run it by double-clicking!
