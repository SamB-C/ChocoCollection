import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

# Configuration
fs = 44100          # Sample rate
seconds = 5         # Duration of recording
output_file = "output.wav"

# List available devices
print("Available audio devices:")
print(sd.query_devices())
print()

# Use built-in microphone as input (device 0 from your debug)
input_device = 0
output_device = 1  # Built-in Output (speakers)

# Check device info
dev_info = sd.query_devices(input_device)
num_channels = dev_info['max_input_channels']
print(
    f"Recording from device '{dev_info['name']}' with {num_channels} channel(s)")
print()

# Record
print(f"Recording for {seconds} seconds...")
recording = sd.rec(int(seconds * fs),
                   samplerate=fs,
                   channels=num_channels,
                   dtype='int16',
                   device=input_device)
sd.wait()
print("Recording finished!")

# Convert to mono if needed
if num_channels > 1:
    print("Converting stereo to mono...")
    recording_mono = recording.mean(axis=1).astype('int16')
else:
    recording_mono = recording

# Save WAV file
write(output_file, fs, recording_mono)
print(f"Saved recording to '{output_file}'")

# Playback
print("Playing back recording...")
sd.play(recording_mono, samplerate=fs, device=output_device)
sd.wait()
print("Playback finished!")
