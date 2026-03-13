import sys

import files;
import keyboardListener;
import dataTools;
import argparse;
from pynput import keyboard;
import time;
import copy;

def main():
    # parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", required=False, default="0.975", help="The minimum similarity score to be authenticated: [0-1].")
    parser.add_argument("-stats", action="store_true", help="Puts the program in statistics mode.")
    args = parser.parse_args()
    similarityThreshold = float(args.t) 

    # decide on path.
    if (args.stats):
        statsAnalysis()
    else:
        dataCollection(similarityThreshold)

def statsAnalysis():
    # load sampledata
    data: dict[str, dict[str, str | str, list]] = {}
    files.loadSampledata(data)

    while True:

        inFile, inSampleData = False, False
        while (not inFile and not inSampleData):
        # stats for which user
            user = input("Check Stats for which user?\n").strip()
            checkQuit(user)
            user = user.replace(" ", "_")

            # where are stats
            inFile, inSampleData = files.userExists(data, user)
            if (not inFile and not inSampleData):
                print(f"{user} does not exist. Reenter a user.")
        # load data
        if (inFile and data.get(user) == None):
            files.loadUser(data, user)

        # get a simlarity threshold to use.
        similarityThreshold = input("Enter a similarlity threshold between [0-1]\n")
        checkQuit(similarityThreshold)
        similarityThreshold = float(similarityThreshold)

        # get data
        TA = 0
        TR = 0
        FA = 0
        FR = 0
        averageNorm = dataTools.getAverageNorm(data, user)
        if (inSampleData):
            TA, TR, FA, FR = sampleDataStatistics(TA, TR, FA, FR, data, user, averageNorm, similarityThreshold)
        else:
            TA, TR, FA, FR = userDataStatistics(TA, TR, FA, FR, data, user, averageNorm, similarityThreshold)
        
        print(f"TA:{TA}, TR:{TR}, FA:{FA}, FR:{FR}")
        # Probability a legitimate user is accepted
        TAR = TA/(TA+FR) if TA+FR != 0 else 0
        # Probability an imposter is rejected.
        TRR = TR/(TR+FA) if TR+FA != 0 else 0
        # Probability an imposter is authenticated
        FAR = FA/(FA+TR) if FA+TR != 0 else 0
        # Probability a legitimate user is rejected
        FRR = FR/(FR+TA) if TR+TA != 0 else 0
        print(f"True Acceptance Rate (TAR):{TAR*100:.2f}%")
        print(f"True Rejection Rate (TRR):{TRR*100:.2f}%")
        print(f"False Acceptance Rate (FAR):{FAR*100:.2f}%")
        print(f"False Rejection Rate (FRR):{FRR*100:.2f}%")
        input("Press Enter to continue:")
        
def userDataStatistics(
    TA, TR, FA, FR,
    data: dict[str, dict[str, str | str, list]], 
    user: str,
    averageNorm,
    similarityThreshold,
    ):
    for record in data[user]["trueRecords"]:
        TA, TR = AcceptReject(TA, TR, averageNorm, record, similarityThreshold)
    for record in data[user]["falseRecords"]:
        FA, FR = AcceptReject(FA, FR, averageNorm, record, similarityThreshold)
    return TA, TR, FA, FR

                    
def sampleDataStatistics(
    TA, TR, FA, FR,
    data: dict[str, dict[str, str | str, list]], 
    user: str,
    averageNorm,
    similarityThreshold,
    ):
    for userName, userData in data.items():
        if (userData.get("isSampleData") == None):
            continue
        else:
            # True
            if (user == userName):
                for record in userData["trueRecords"]:
                    TA, TR = AcceptReject(TA, TR, averageNorm, record, similarityThreshold)
            # False
            else:
                for record in userData["trueRecords"]:
                    FA, FR = AcceptReject(FA, FR, averageNorm, record, similarityThreshold)
    return TA, TR, FA, FR

def AcceptReject(tallyA: int, tallyR: int, averageNorm, record, similarityThreshold):
    # Accpt
    if (dataTools.getSimilarityScore(averageNorm, record) > similarityThreshold):
        tallyA = tallyA+1
    # Reject
    else:
        tallyR = tallyR+1
    return tallyA, tallyR

# --- DATA COLLECTION FLOW ---

def dataCollection(similarityThreshold: float):
    # load sampledata
    data = {}
    files.loadSampledata(data)

    # get the user
    currentUser = input("Enter your username.\n").strip()
    checkQuit(currentUser)

    # load the user if they exist.
    currentUser = currentUser.replace(" ", "_")
    inFile, inSampleData = files.userExists(data, currentUser)
    if (inFile):
        files.loadUser(data, currentUser)
    # make passphrase and create user.
    elif(not inSampleData):
        behaviorPhrase = input("\nCreating newUser.\nEnter A behavioral phrase to use for authentication.\n")+"\n"
        checkQuit(behaviorPhrase)
        files.createUser(data, currentUser, behaviorPhrase)
    
    # last case is the user is already loaded from sampledata

    # print(data[currentUser])
    # confirm the user is who they say they are.
    trueUser = -1
    while (trueUser == -1):
        userInput = input(f"\nAre you actually {currentUser}: Y/N\n")
        checkQuit(userInput)
        trueUser = checkAffirmativeInput(userInput)
        if (trueUser == -1):
            print("invalid Input")
    trueUser = bool(trueUser)

    ## IMPLEMENT AVERAGE
    # average = data.average(data, currentUser)

    # start keyboard listener
    recorder = keyboardListener.keyboardRecorder()
    listener = keyboard.Listener(
        on_press=recorder.on_press, on_release=recorder.on_release)
    listener.start()

    while True:
        print("\nEnter behavior phrase:")
        print(data[currentUser]["behaviorPhrase"], end="")
        finalInput, record = getResultAndRecord(recorder)
        checkQuit(finalInput)
        stringRecord = files.recordToString(record, trueUser)
        match = files.match(finalInput, data[currentUser]["behaviorPhrase"])
        # similarity = 0
        if (not match):
            print(f"\ninput doesn't match behavior phrase: {repr(finalInput)} != {repr(data[currentUser]["behaviorPhrase"])}")
            time.sleep(0.5)
        else:
            averageNorm = dataTools.getAverageNorm(data, currentUser)
            similarity = dataTools.getSimilarityScore(averageNorm, record)
            print(f"\nSimilarity Score: {similarity}")
            if (similarity == None):
                print("Not enough data to authenticate")
            elif (similarity>similarityThreshold):
                print("Authentication: Granted")
            else:
                print("Authentication: Denied")

            files.save(currentUser, stringRecord)
            dataTools.updateData(data, currentUser, record, trueUser)
            time.sleep(0.5)
        
def getResultAndRecord(recorder: keyboardListener.keyboardRecorder):
    # wait until done
    while (not recorder.done):
        time.sleep(0.01)
    # gather result
    finalString = "".join(recorder.inputStr)
    finalRecord = dataTools.formatRecord(copy.deepcopy(recorder.record))
    # reset for next one
    recorder.inputStr.clear()
    recorder.record.clear()
    recorder.done = False
    # return results
    return finalString, finalRecord
    
# returns 1 for positive 0 for negative and -1 for not sure.
def checkAffirmativeInput(input: str):
    input = input.split()[0].lower()
    positives = ["true", "yes", "y"]
    negatives = ["false", "no", "n"]
    for positive in positives:
        if (positive in input):
            return 1
    for negative in negatives:
        if (negative in input):
            return 0
    return -1

def checkQuit(input: str):
    input = input.strip()
    if (input == 'q'):
        exit(0)

if (__name__ == "__main__"):
    main()