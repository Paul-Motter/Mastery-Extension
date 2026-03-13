
def updateData(data: dict[str, dict[str, str | str, list]], name: str, record: str, isUser: bool):
    # Record is from true user.
    if isUser:
        data[name]["trueRecords"].append(record)
    # Record is from a false user.
    else:
        data[name]["falseRecords"].append(record)

def getAverageNorm(data: dict[str, dict[str, str | str, list]], name: str):
    if (len(data[name]["trueRecords"])==0):
        return None
    average = getAverage(data, name)
    return normalize(average)
    
def getSimilarityScore(averageNorm: list, record: list):
    if (averageNorm == None):
        return None
    recordNorm = normalize(record)
    similarityScore = (dot(averageNorm, recordNorm)+1)/2.0
    return similarityScore

# returns the average for the records for a specific user.
# returns none if there are no records available.
def getAverage(data: dict[str, dict[str]], name: str):
    # make sure there are records
    sumRecords = [0] * len(data[name]["trueRecords"][0]) if len(data[name]["trueRecords"]) > 0 else None
    if (sumRecords == None):
        raise Exception(f"Cannot average with no data for {name}")
    numRecords = len(data[name]["trueRecords"])
    # gather and sum and number of records
    for record in data[name]["trueRecords"]:
        numRecords = numRecords+1
        for i in range(0,len(record)):
            sumRecords[i]=sumRecords[i]+record[i]
    # average the results
    average = [element/numRecords for element in sumRecords]
    return average

def normalize(recordAverage: list[float]):
    # get magnitude
    sumSquares = 0
    for element in recordAverage:
        # sumSquares+=pow(float(element), 2) 
        sumSquares+=pow(element, 2) 
    magnitude = pow(sumSquares, 0.5)
    # normalize
    normalized = []
    for i in range(0, len(recordAverage)):
        # normalized.append(float(recordAverage[i])/magnitude)
        normalized.append(recordAverage[i]/magnitude)
    return normalized

def dot(vec1: list[float], vec2: list[float]):
    result = 0
    if (len(vec1) != len(vec2)):
        raise Exception(f"vector length mismatch: {len(vec1)}!={len(vec2)}")
    for i in range(0, len(vec1)):
        result += vec1[i]*vec2[i]
    return result

###
# H = (release-press)total time held town 
# DD = (pressCurrent-pressPrev)
# UD = (pressCurrent-releasePrev)
def formatRecord(record: list[dict]):
    # repeated order = H, DD, UD
    recordFormatted: list[float] = []
    lastPress = None
    lastRelease = None
    for entry in record:
        pressT= entry["press"]
        releaseT = entry["release"]
        # H
        recordFormatted.append(releaseT-pressT)
        # DD
        if (lastPress != None):
            recordFormatted.append(pressT-lastPress)
        # UD
        if (lastRelease != None):
            recordFormatted.append(pressT-lastRelease)
        
        lastPress = pressT
        lastRelease = releaseT
    return recordFormatted
        
            