import sounddevice as sd
import soundfile as sf
import os
import sys
from ChocoModules import playback_bar, recognize_number_from_mic
import threading
from rich import print

filename = str(recognize_number_from_mic()) + ".wav"

# Check if file exists
if not os.path.exists(filename):
    print(f"[ERROR] File '{filename}' does not exist!")
    sys.exit(1)

# Start progress bar in a separate thread
playback_bar_complete = threading.Event()


try:
    with sf.SoundFile(filename, 'r') as file:
        duration_seconds = len(file) / file.samplerate
        print(f"[INFO] Playing '{filename}'")
        print(f"        Sample rate: {file.samplerate} Hz")
        print(f"        Channels: {file.channels}")
        print(f"        Frames: {len(file)}")
        print(f"        Duration: {duration_seconds:.2f} seconds")
        print()
        threading.Thread(target=lambda: playback_bar(
            duration_seconds, playback_bar_complete), daemon=True).start()
        # Open a continuous OutputStream
        with sd.OutputStream(samplerate=file.samplerate,
                             channels=file.channels,
                             dtype='float32') as stream:
            blocksize = 1024
            for block in file.blocks(blocksize=blocksize, dtype='float32'):
                # write directly to stream without stopping
                stream.write(block)

        while not playback_bar_complete.is_set():
            sd.sleep(100)

        print("[INFO] Playback finished successfully!")

except Exception as e:
    print(f"[ERROR] Playback failed: {e}")
    sys.exit(1)
