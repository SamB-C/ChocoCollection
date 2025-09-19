import sys
from ChocoModules import get_recording, play_back, recognize_number_from_mic, play_wav, get_answer_to_prompt, check_inside_venv, get_script_dir, save_recording
from rich import print
import os


def main():
    script_dir = get_script_dir()

    # Play introduction
    play_wav(f"{script_dir}/narration/WelcomeInput.wav")
    # Get number
    number = recognize_number_from_mic()
    if number == None:
        play_wav(f"{script_dir}/narration/NotRecognised.wav")
        print("[red]Invalid number recognized, exiting.[/red]")
        sys.exit(1)
    # Get all WAV file numbers
    wav_files = [int(f.split(".")[0])
                 for f in os.listdir(".") if f.endswith(".wav")]
    if number in wav_files:
        print(f"WAV file for number {number} already exists.")
        answer = None
        count = 0
        while answer == None and count < 100:
            answer = get_answer_to_prompt(
                f"{script_dir}/narration/NumberTaken.wav", "This number has already been taken. Say 'Override' to continue anyway, or 'Cancel' to cancel.", ["override", "over", "cancel"])
            if answer == "cancel":
                print("Operation cancelled.")
                sys.exit(1)
            elif answer in ["override", "over"]:
                print("Overriding existing number.")
                break
            count += 1
        if count == 100:
            print("[red]Too many attempts. Exiting.[/red]")
            sys.exit(1)

    output_file = f"{script_dir}/{number}.wav"
    recording_mono, fs, duration_seconds = get_recording()
    save_recording(output_file, recording_mono, fs)

    # ---------------- Playback ----------------

    play_back(recording_mono, fs, duration_seconds)


if __name__ == "__main__":
    check_inside_venv()
    main()
