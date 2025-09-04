import sounddevice as sd
import soundfile as sf
import os
import sys
import numpy as np

filename = "output.wav"

# Check if file exists
if not os.path.exists(filename):
    print(f"[ERROR] File '{filename}' does not exist!")
    sys.exit(1)

try:
    with sf.SoundFile(filename, 'r') as file:
        print(f"[INFO] Playing '{filename}'")
        print(f"        Sample rate: {file.samplerate} Hz")
        print(f"        Channels: {file.channels}")
        print(f"        Frames: {len(file)}")

        # Open a continuous OutputStream
        with sd.OutputStream(samplerate=file.samplerate,
                             channels=file.channels,
                             dtype='float32') as stream:
            blocksize = 1024
            for block in file.blocks(blocksize=blocksize, dtype='float32'):
                # write directly to stream without stopping
                stream.write(block)

        print("[INFO] Playback finished successfully!")

except Exception as e:
    print(f"[ERROR] Playback failed: {e}")
    sys.exit(1)
