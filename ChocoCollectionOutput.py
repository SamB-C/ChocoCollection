from ChocoModules import recognize_number_from_mic, play_wav

play_wav("6.wav")
filename = str(recognize_number_from_mic()) + ".wav"
play_wav(filename)
