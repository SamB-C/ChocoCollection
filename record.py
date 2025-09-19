import sys
from ChocoModules import check_inside_venv, get_recording, get_script_dir, get_answer_to_prompt, play_back, play_recording_countdown, save_recording
import os

check_inside_venv()

# Get first argument
output_file = None
try:
    output_file = sys.argv[1]
except IndexError:
    print("No output file specified. Exiting.")
    sys.exit(1)

script_dir = get_script_dir()
output_file = f"{script_dir}/narration/{output_file}.wav"
print(f"Output file: {output_file}")

# Check override
try:
    override = sys.argv[2]
    if override.lower() != "override":
        print("To override existing file, pass 'override' as second argument.")
        sys.exit(1)
    else:
        print("Override enabled.")
except IndexError:
    if os.path.exists(output_file):
        answer = None
        count = 0  # Safety counter
        while answer == None and count < 100:
            answer = get_answer_to_prompt(
                f"{script_dir}/narration/NumberTaken.wav", "This number has already been taken. Say 'Override' to continue anyway, or 'Cancel' to cancel.", ["override", "over", "cancel"])
            if answer == "override" or answer == "over":
                print("Continuing with override...")
                break
            else:
                print("Operation cancelled.")
                sys.exit(1)
            count += 1
        if count == 100:
            print("[red]Too many attempts. Exiting.[/red]")
            sys.exit(1)


backup_counter = 0
recording = None
fs = None
while backup_counter < 100:
    #  Record
    recording, fs, duration_seconds = get_recording()

    # Play back
    play_back(recording, fs, duration_seconds)

    # Confirm user is happy
    answer = get_answer_to_prompt(f"{script_dir}/narration/ConfirmRecording.wav",
                                  "Are you happy with the recoding? Say 'Confirm' to confirm, or 'Redo' to redo.", ["confirm", "redo"])

    if answer == "confirm":
        print("Recording confirmed.")
        break
    else:
        print("Redoing recording...")

    backup_counter += 1

if backup_counter == 100:
    print("Too many attempts. Exiting.")
    sys.exit(1)

print("Saving recording...")
save_recording(output_file, recording, fs)
