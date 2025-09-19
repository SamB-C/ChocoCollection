# Potential Errors (Dependencies)

When installing PyAudio, portaudio needs to be installed first:
`brew install portaudio`.

# WAV files

Errors:
NotRecognised - "This number was not recognised"
NumberTaken - "This number has already been taken. Say 'Override' to continue anyway, or 'Cancel' to cancel."
Countdown:
3, 2, 1 - Me saying the numbers 3, 2, and 1 respectively.
RecordingIn - "Recording in"
SayNumber - "Please say your number, now:"
Introduction:
WelcomeOutput - "Welcome to the Chocolate Bank. Shortly, say the number on the chocolate to check it out."
WelcomeInput - "Welcome to the Chocolate Bank recording service. To check in a chocolate as a number, say the number, then record its fun fact."
Misc:
Delete - "Would you like to delete this number? Say 'Delete' to delete, or 'Cancel' to exit the program."
ConfirmRecording - "Are you happy with the recoding? Say 'Confirm' to confirm, or 'Redo' to redo."
10 - Spare number (Must stay spare)

WAV files > 10 are audio files that can be linked to chocolate bars.
This is because numbers that are spoken in 1 syllable are not picked up by the speech to text.

To record a wav file with a different name, provide it as an argument to the script ChocoCollectionInput.py

All WAV files must be numbers (ie a set of digits followed by .wav) or line 24 in ChocoCollectionInput.py will break
