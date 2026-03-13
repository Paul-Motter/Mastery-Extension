from os import path

# ".tie5Roanl"
# loads the data from the sampledata
def loadSampledata(data: dict[str, dict[str, str | str, list]]):
    password = ".tie5Roan1"
    with open("data/SampleData.csv", "r") as f:
        header = f.readline().strip().split(",")
        for row in f:
            row = row.strip().split(",")
            # formattedRow = row[3:]
            formattedRow = [float(x) for x in row[3:]]
            if (data.get(row[0]) == None):
                data[row[0]] = {
                    "behaviorPhrase": password,
                    "isSampleData": True,
                    "trueRecords": [],
                }
            data[row[0]]["trueRecords"].append(formattedRow)
    return password

# checks if a user exists in the sampledata or other files.
def userExists(data: dict[str, dict[str, str | str, list]], name: str):
    inFile = path.exists(f"data/{name}.csv")
    inSampleData = not (data.get(name) == None or data.get(name).get("isSampleData") == None)
    return inFile, inSampleData

# create the user file and add it to data.
def createUser(data: dict[str, dict[str, str | str, list]], name: str, behaviorPhrase: str):
    with open(f"data/{name}.csv", "x") as f:
        f.write(f"{behaviorPhrase}\n")
    data[name] = {
        "behaviorPhrase": behaviorPhrase,
        "trueRecords": [],
        "falseRecords": [],
    }

# loads a user file
def loadUser(data: dict[str, dict[str, str | str, list]], name: str):
    with open(f"data/{name}.csv", "r") as f:
        # create data entry
        data[name] = {
            "behaviorPhrase": f.readline(),
            "trueRecords": [],
            "falseRecords": [],
        }
        # read blank line between behavioralPhrase and first data.
        f.readline()
        # fill the records
        for row in f:
            # get row and take off the first element.
            record = [float(x) for x in row.strip().split(",")[1:]]
            # Record is from true user.
            if row.startswith("T"):
                data[name]["trueRecords"].append(record)
            # Record is from a false user.
            else:
                data[name]["falseRecords"].append(record)
        
def match(finalInput, behaviorPhrase):
    return finalInput == behaviorPhrase

def save(name: str, formattedRecord: str):
    with open(f"data/{name}.csv", "a") as f:
        f.write(formattedRecord)

def recordToString(record: list[float], trueUser: bool):
    trueOrFalse = "T" if trueUser else "F"
    return f"{trueOrFalse},{"".join((f"{x}," for x in record)).strip(",")+"\n"}"
