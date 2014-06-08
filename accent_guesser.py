#!/bin/python
import sys, os, random, subprocess

def choose_wav_file(wav_dir, langs):
    lang = random.choice(langs)
    lang_dir = os.path.join(wav_dir, lang)
    wav_file = random.choice(os.listdir(lang_dir))
    return os.path.join(lang_dir, wav_file)

def print_log(stats):
    numAnswers = len(stats["humanAnswers"])
    if numAnswers == 0:
        print "No responses yet.\n"
    else:
        print "\nHuman answers: (Native language, Guessed native language)"
        for tup in stats["humanAnswers"]:
            print tup[0] + "\t" + tup[1]
        print "Correct: {0} out of {1} ({2:.1f}%)\n".format(stats["humanCorrect"], numAnswers, stats["humanCorrect"] * 100.0 / numAnswers)
        print "Machine answers: (Native language, Guessed native language)"
        for tup in stats["machineAnswers"]:
            print tup[0] + "\t" + tup[1]
        print "Correct: {0} out of {1} ({2:.1f}%)\n".format(stats["machineCorrect"], numAnswers, stats["machineCorrect"] * 100.0 / numAnswers)

def ask_user_to_continue(stats):
    while True:
        answer = raw_input("Press enter to guess an accent, press q to quit, or press l for log: ")
        if answer.lower() == "l":
            print_log(stats)
        elif len(answer) == 0:
            return True
        elif answer.lower() == "q" or answer.lower() == "quit":
            return False
        else:
            return True

def get_lang_and_id(path):
    filename = path.split("/")[-1]
    tokens = filename.split("-")
    lang = tokens[0].capitalize()
    gender_and_id = tokens[1].split(".")[0]
    return lang, int(gender_and_id[1:])

def print_options(langs):
    for i in range(len(langs)):
        print "{} = {}".format(str(i+1).ljust(2), langs[i].capitalize())

def isValidNumber(response, max_val):
    try:
        val = int(response)
        return val in range(1, max_val + 1)
    except ValueError:
        return False

def wait_for_response(wav_file, langs):
	process = subprocess.Popen(["afplay", wav_file])
	response = ""
	max_lang = len(langs)
	while True:
		response = raw_input("Choose a language (1-"+str(max_lang)+") or press 'P' to play again: ")
		if isValidNumber(response, max_lang):
			process.terminate()
			return langs[int(response) - 1]
		elif len(response) > 0 and response[0].lower() == "p":
			process.terminate()
			process = subprocess.Popen(["afplay", wav_file])

def prompt_num_langs():
    response = ""
    validChoices = ["5", "10", "15"]
    while True:
        response = raw_input("How many languages would you like to include (5, 10, 15): ")
        if response not in validChoices:
            print "Sorry, you must play with 5, 10 or 15 languages."
        else:
            return int(response)

def get_machine_guesses(numLangs, labelDict):
    predFile = open('nonaligned/predictions/' + str(numLangs) + '.txt')
    lines = predFile.readlines()
    predFile.close()
    guesses = {}
    for line in lines:
        tokens = line.split()
        guess = labelDict[int(tokens[2])]
        guesses[int(tokens[0])] = guess
    return guesses

def accent_guesser_loop(wav_dir, labelDict):
    print "\nWelcome to Accent Guesser, where you try to guess the native language of a foreign-accented English utterance."
    numLangs = prompt_num_langs()
    print "Setting up a game with {} languages...\n".format(str(numLangs))
    machineDict = get_machine_guesses(numLangs, labelDict) # Speaker id -> language string guess
    all_langs = ['arabic', 'mandarin', 'turkish', 'spanish', 'russian',
         'dutch', 'korean', 'french', 'german', 'portuguese',
         'italian', 'japanese', 'polish', 'cantonese', 'macedonian']
    langs = all_langs[:numLangs]
    stats = {"humanAnswers": [], "humanCorrect": 0, "machineAnswers": [], "machineCorrect": 0}

    while ask_user_to_continue(stats):
        wav_file = choose_wav_file(wav_dir, langs)
        lang, speaker_id = get_lang_and_id(wav_file)
        print_options(langs)
        response = wait_for_response(wav_file, langs)
        machineGuess = machineDict[speaker_id]
        stats["humanAnswers"].append((lang.lower(), response.lower()))
        stats["machineAnswers"].append((lang.lower(), machineGuess.lower()))

        print "\nYou guessed {} and the computer guessed {}.".format(response.capitalize(), machineGuess.capitalize())

        if machineGuess.lower() == lang.lower():
            stats["machineCorrect"] += 1

        if response.lower() == lang.lower():
            print "Congratulations! That was indeed {}.".format(lang.capitalize())
            stats["humanCorrect"] += 1
        else:
            print "Sorry! That was actually {}.".format(lang.capitalize())

        numRounds = len(stats["humanAnswers"])
        print "Score after {} {}: computer {}, you {}.\n".format(
            str(numRounds), 'round' if numRounds==1 else 'rounds',
            str(stats["machineCorrect"]), str(stats["humanCorrect"]))


if __name__ == "__main__":
    wav_dir = "nonaligned/wav" if len(sys.argv) <= 1 else sys.argv[1]
    labelDict = {
        0: 'arabic',
        1: 'cantonese',
        2: 'dutch',
        3: 'french',
        4: 'german',
        5: 'italian',
        6: 'japanese',
        7: 'korean',
        8: 'macedonian',
        9: 'mandarin',
        10: 'polish',
        11: 'portuguese',
        12: 'russian',
        13: 'spanish',
        14: 'turkish'
    }
    accent_guesser_loop(wav_dir + "/", labelDict)
