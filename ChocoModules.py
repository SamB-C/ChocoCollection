import sys
import time
import speech_recognition as sr
import numpy as np
import sounddevice as sd

DIGITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
}

# ---------------- Main function ----------------


def get_number_from_text(text):
    if text in DIGITS.keys():
        return DIGITS[text]
    else:
        return int(text)


def play_number_back(audio):
    # Convert AudioData to numpy array
    raw_data = np.frombuffer(audio.get_raw_data(), dtype=np.int16)
    sample_rate = audio.sample_rate

    # Play back the recording
    print("Playing back your recording...")
    sd.play(raw_data, samplerate=sample_rate)
    sd.wait()


def recognize_number_from_mic():
    r = sr.Recognizer()
    audio = None
    try:
        with sr.Microphone() as source:
            print("[DEBUG] Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
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
        play_number_back(audio)
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
