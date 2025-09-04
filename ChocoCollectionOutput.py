from ChocoModules import recognize_number_from_mic, play_wav, get_answer_to_prompt

play_wav("narration/WelcomeOutput.wav")
filename = str(recognize_number_from_mic()) + ".wav"
play_wav(filename)

answer = None
while answer == None:
    answer = get_answer_to_prompt(
        "narration/Delete.wav", "Would you like to delete this number? Say 'Delete' to delete, or 'Cancel' to exit the program.", ["delete", "cancel"])
    if answer == "cancel":
        print("[INFO] Operation cancelled by user.")
        break
    elif answer == "delete":
        print("[INFO] User chose to delete the number.")
        break
