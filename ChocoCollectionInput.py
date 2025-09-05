import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import sys
import time
from ChocoModules import playback_bar, recognize_number_from_mic, play_wav, play_wav_quiet, get_answer_to_prompt
from rich import print
import os

number = "narration/void"  # Default number if none recognized
try:
    number = "narration/" + sys.argv[1]
except IndexError:
    # Play introduction
    play_wav("narration/WelcomeInput.wav")
    # Get number
    number = recognize_number_from_mic()
    if number == 0:
        play_wav("narration/NotRecognised.wav")
        print("Invalid number recognized, exiting.")
        sys.exit(1)
    # Get all WAV file numbers
    wav_files = [int(f.split(".")[0])
                 for f in os.listdir(".") if f.endswith(".wav")]
    if number in wav_files:
        print(f"WAV file for number {number} already exists.")
        answer = None
        while answer == None:
            answer = get_answer_to_prompt(
                "narration/NumberTaken.wav", "This number has already been taken. Say 'Override' to continue anyway, or 'Cancel' to cancel.", ["override", "over", "cancel"])
            if answer == "cancel":
                print("Operation cancelled.")
                sys.exit(1)
            elif answer in ["override", "over"]:
                print("Overriding existing number.")
                break


# ---------------- Configuration ----------------
fs = 44100                  # Sample rate
max_seconds = 30            # Maximum duration (30 seconds)
output_file = f"{number}.wav"


# ---------------- List devices ----------------
print("Available audio devices:")
print(sd.query_devices())
print()

# Default input/output devices
input_device = 0   # Built-in Microphone
output_device = 1  # Built-in Output (speakers)

dev_info = sd.query_devices(input_device)
num_channels = dev_info['max_input_channels']
print(
    f"Recording from device '{dev_info['name']}' with {num_channels} channel(s)")
print(f"Maximum duration: {max_seconds} seconds")
print()

# ---------------- Recording ----------------
recorded_chunks = []


def callback(indata, frames, time, status):
    if status:
        print(f"[red]WARNING {status}[/red]")
    recorded_chunks.append(indata.copy())


# Play a sound to indicate start of recording
play_wav_quiet("narration/RecordingIn.wav", False)
print("Recording in:")
escape_codes = ['bold red', 'bold yellow', 'bold green']  # Red, Yellow, Green
for i in range(3, 0, -1):
    play_wav_quiet(f"narration/{i}.wav")
    time.sleep(0.2)
    print(f"[{escape_codes[i-1]}]{i}...[/{escape_codes[i-1]}]\n\n", end="")
    sys.stdout.flush()
    time.sleep(1)
print("[bold purple]Recording...[/bold purple]")

print("Press [bold red]Enter to stop[/bold red] or wait for maximum duration ([blue]30s[/blue]).", end="")

# Stop event setup
stop_flag = threading.Event()


def wait_for_enter():
    input()
    stop_flag.set()


# Start thread to listen for Enter key
threading.Thread(target=wait_for_enter, daemon=True).start()
try:
    with sd.InputStream(samplerate=fs, channels=num_channels, dtype='int16',
                        device=input_device, callback=callback):
        total_frames = 0
        blocksize = 1024
        while not stop_flag.is_set() and total_frames < max_seconds * fs:
            sd.sleep(100)  # sleep briefly to reduce CPU usage
            total_frames += 100
except Exception as e:
    print(f"[red]Recording failed:[/red] {e}")
    sys.exit(1)

# Combine all recorded chunks
if not recorded_chunks:
    print("[red]No audio recorded![/red]")
    sys.exit(1)

recording = np.concatenate(recorded_chunks)
num_frames = len(recording)  # total number of samples
duration_seconds = num_frames / fs
print(f"Recorded {duration_seconds:.2f} seconds of audio")

# ---------------- Convert to mono if needed ----------------
if num_channels > 1:
    print("Converting stereo to mono...")
    recording_mono = recording.mean(axis=1).astype('int16')
else:
    recording_mono = recording

# ---------------- Save WAV ----------------
try:
    write(output_file, fs, recording_mono)
    print(f"Saved recording to '{output_file}'")
except Exception as e:
    print(f"[red]Failed to save WAV file:[/red] {e}")
    sys.exit(1)

# ---------------- Playback ----------------

progressBarComplete = threading.Event()


try:
    print("Playing back recording...\n")
    threading.Thread(target=lambda: playback_bar(duration_seconds,
                                                 progressBarComplete), daemon=True).start()
    sd.play(recording_mono, samplerate=fs, device=output_device)
    sd.wait()
    while not progressBarComplete.is_set():
        time.sleep(0.1)
except Exception as e:
    print(f"[red]Playback failed:[/red] {e}")
    sys.exit(1)
