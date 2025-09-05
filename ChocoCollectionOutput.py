from ChocoModules import recognize_number_from_mic, play_wav, get_answer_to_prompt, get_script_dir
import os

script_dir = get_script_dir()

play_wav(f"{script_dir}/narration/WelcomeOutput.wav")
filename = script_dir + "/" + str(recognize_number_from_mic()) + ".wav"
play_wav(filename)

answer = None
while answer == None:
    answer = get_answer_to_prompt(
        f"{script_dir}/narration/Delete.wav", "Would you like to delete this number? Say 'Delete' to delete, or 'Cancel' to exit the program.", ["delete", "cancel"])
    if answer == "cancel":
        print("Operation cancelled.")
        break
    elif answer == "delete":
        os.remove(filename)
        print("Number deleted.")
        break
