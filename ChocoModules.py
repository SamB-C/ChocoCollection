import sys
import time
import speech_recognition as sr
import numpy as np
import sounddevice as sd
import os
import threading
import sounddevice as sd
import soundfile as sf
from rich import print


def get_number_from_text(text):
    return int(text)


def play_audio_back(audio):
    # Convert AudioData to numpy array
    raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    sample_rate = audio.sample_rate

    # Play back the recording
    print("Playing back your recording...")
    sd.play(raw_data, samplerate=sample_rate)
    sd.wait()


def get_answer_to_prompt(prompt, prompt_text, answers):
    r = sr.Recognizer()
    audio = None
    try:
        with sr.Microphone() as source:
            print("[DEBUG] Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            play_wav(prompt)
            print(prompt_text)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("[ERROR] No speech detected within timeout")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to access microphone: {e}")
        return None

    try:
        text = r.recognize_google(audio)
        print(f"[DEBUG] Recognized speech: '{text}'")
        if text.lower() in answers:
            print(f"[DEBUG] Matched answer: {text.lower()}")
            play_audio_back(audio)
            return text.lower()
        else:
            print(f"[DEBUG] No match for recognized text: '{text.lower()}'")
            return None
    except sr.UnknownValueError:
        print("[ERROR] Could not understand audio")
    except sr.RequestError as e:
        print(f"[ERROR] Could not request results from Google API: {e}")
    return 0


def recognize_number_from_mic():
    r = sr.Recognizer()
    audio = None
    try:
        with sr.Microphone() as source:
            print("[DEBUG] Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            # Play "Please say a natural number, now: "
            play_wav("narration/SayNumber.wav")
            print("Please say a natural number:")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("[ERROR] No speech detected within timeout")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to access microphone: {e}")
        return None

    try:
        text = r.recognize_google(audio)
        print(f"[DEBUG] Recognized speech: '{text}'")
        number = get_number_from_text(text.lower())
        print(f"[DEBUG] Converted to integer: {number}")
        play_audio_back(audio)
        return number
    except sr.UnknownValueError:
        print("[ERROR] Could not understand audio")
    except sr.RequestError as e:
        print(f"[ERROR] Could not request results from Google API: {e}")
    return 0


def playback_bar(duration_seconds, barCompleteEvent=None):
    total = 100  # total iterations
    for i in range(total + 1):
        percent = i / total
        bar_length = 40
        filled_length = int(bar_length * percent)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        sys.stdout.write(f'\rPlaying: |{bar}| {percent*100:.1f}%')
        sys.stdout.flush()
        time.sleep(duration_seconds/total)  # simulate work
    print("\nPlayback finished!")
    print()  # new line after completion
    if barCompleteEvent != None:
        barCompleteEvent.set()


def play_wav(filename):
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


def play_wav_quiet(filename, alternate_thread=True):
    """ Play a WAV in a seperate thread, without printing any information """
    # Check if file exists
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' does not exist!")
        sys.exit(1)

    def play_file():
        try:
            with sf.SoundFile(filename, 'r') as file:
                # Open a continuous OutputStream
                with sd.OutputStream(samplerate=file.samplerate,
                                     channels=file.channels,
                                     dtype='float32') as stream:
                    blocksize = 1024
                    for block in file.blocks(blocksize=blocksize, dtype='float32'):
                        # write directly to stream without stopping
                        stream.write(block)

        except Exception as e:
            print(f"[ERROR] Playback failed: {e}")
            sys.exit(1)

    if alternate_thread:
        threading.Thread(target=play_file, daemon=True).start()
    else:
        play_file()
