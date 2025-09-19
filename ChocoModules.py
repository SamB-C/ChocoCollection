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
import sys
from pathlib import Path


def get_script_dir():
    return os.path.dirname(os.path.abspath(__file__))


def check_inside_venv():
    # Path to your project's venv (adjust if needed)
    VENV_PATH = Path(__file__).parent / "venv"

    # Check if we're running inside the venv
    real_prefix = getattr(sys, "real_prefix", None) or getattr(
        sys, "base_prefix", sys.prefix)

    if not str(VENV_PATH) in sys.prefix:
        print(f"""
    You are not running inside the expected virtual environment!

    Expected venv: {VENV_PATH}
    Current sys.prefix: {sys.prefix}

    Please run the program using:
        source .venv/bin/activate
    or
        ./run.sh
    """)
        sys.exit(1)


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
    """ Play a prompt and listen for one of the specified answers. Returns the matched answer in lowercase, or None if no match. """
    r = sr.Recognizer()
    audio = None
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            play_wav(prompt)
            print(prompt_text)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("[red]No speech detected within timeout[/red]")
        return None
    except Exception as e:
        print(f"[red]Failed to access microphone:[/red] {e}")
        return None

    try:
        text = r.recognize_google(audio)
        print(f"Recognized speech: [bold purple]'{text}'[/bold purple]")
        if text.lower() in answers:
            print(f"Matched answer: [bold green]{text.lower()}[/bold green]")
            play_audio_back(audio)
            return text.lower()
        else:
            print(
                f"No match for recognized text: [/bold red]'{text.lower()}'[/bold red]")
            return None
    except sr.UnknownValueError:
        print("[red]Could not understand audio[/red]")
        return None
    except sr.RequestError as e:
        print(f"[red]Could not request results from Google API:[red] {e}")
        return None
    return 0


def recognize_number_from_mic():
    r = sr.Recognizer()
    audio = None
    try:
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            # Play "Please say a natural number, now: "
            play_wav(f"{get_script_dir()}/narration/SayNumber.wav")
            print("Please say a natural number:")
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
    except sr.WaitTimeoutError:
        print("[red]No speech detected within timeout.[/red]")
        return None
    except Exception as e:
        print(f"[red]Failed to access microphone:[/red] {e}")
        return None

    try:
        text = r.recognize_google(audio)
        print(f"Recognized speech: [bold purple]'{text}'[/bold purple]")
        number = get_number_from_text(text.lower())
        print(f"Converted to integer: [bold green]{number}[/bold green]")
        play_audio_back(audio)
        return number
    except sr.UnknownValueError:
        print("[red]Could not understand audio[/red]")
    except sr.RequestError as e:
        print(f"[red]Could not request results from Google API:[/red] {e}")
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
        print(f"[red]File [bold]'{filename}'[/bold] does not exist![/red]")
        sys.exit(1)

    # Start progress bar in a separate thread
    playback_bar_complete = threading.Event()

    try:
        with sf.SoundFile(filename, 'r') as file:
            duration_seconds = len(file) / file.samplerate
            print(f"Playing '{filename}'")
            print(f"\tSample rate: {file.samplerate} Hz")
            print(f"\tChannels: {file.channels}")
            print(f"\tFrames: {len(file)}")
            print(f"\tDuration: {duration_seconds:.2f} seconds")
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

            print("Playback finished successfully!")

    except Exception as e:
        print(f"[red]Playback failed:[/red] {e}")
        sys.exit(1)


def play_wav_quiet(filename, alternate_thread=True):
    """ Play a WAV in a seperate thread, without printing any information """
    # Check if file exists
    if not os.path.exists(filename):
        print(f"[red]File [bold]'{filename}'[/bold] does not exist![/red]")
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
            print(f"[red]Playback failed:[/red] {e}")
            sys.exit(1)

    if alternate_thread:
        threading.Thread(target=play_file, daemon=True).start()
    else:
        play_file()
