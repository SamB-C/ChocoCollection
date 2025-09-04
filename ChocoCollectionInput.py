import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import sys
import time
from ChocoModules import playback_bar

# ---------------- Configuration ----------------
fs = 44100                  # Sample rate
max_seconds = 30            # Maximum duration (30 seconds)
output_file = "output.wav"

# ---------------- Stop event setup ----------------
stop_flag = threading.Event()


def wait_for_enter():
    input("Press Enter to stop recording...\n")
    stop_flag.set()


# Start thread to listen for Enter key
threading.Thread(target=wait_for_enter, daemon=True).start()

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
        print(f"[WARNING] {status}")
    recorded_chunks.append(indata.copy())


print("Recording... Press Enter to stop or wait for maximum duration (30s).")
try:
    with sd.InputStream(samplerate=fs, channels=num_channels, dtype='int16',
                        device=input_device, callback=callback):
        total_frames = 0
        blocksize = 1024
        while not stop_flag.is_set() and total_frames < max_seconds * fs:
            sd.sleep(100)  # sleep briefly to reduce CPU usage
            total_frames += 100
except Exception as e:
    print(f"[ERROR] Recording failed: {e}")
    sys.exit(1)

# Combine all recorded chunks
if not recorded_chunks:
    print("[ERROR] No audio recorded!")
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
    print(f"[ERROR] Failed to save WAV file: {e}")
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
    print(f"[ERROR] Playback failed: {e}")
    sys.exit(1)
