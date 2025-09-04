import sys
import time


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
