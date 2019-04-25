import json
import glob
import nltk
import extractweatherclimate
import extractroadtypedirection

def TokenizePOSTaggedParagrapgh(summary):
    taggedList=[]
    summ_text = nltk.sent_tokenize(summary)  # this gives us a list of sentences
    # now loop over each sentence and tokenize it separately
    for sentence in summ_text:
        tokenized_text = nltk.word_tokenize(sentence)
        tagged = nltk.pos_tag(tokenized_text)
        taggedList.append(tagged)
        #print(tagged)

    return taggedList


def TokenizeParagraph(summary):
    summList = nltk.sent_tokenize(summary) # Untagged Senestences
    print(summList)
    return summList


def GetSummaryFromJSONFiles():
    jsonFiles = glob.glob("../resources/summary/*.json")
    for jsonFile in jsonFiles:     # read all the JSON Files.
        summDict = {}
        with open(jsonFile) as json_file:
            data = json.load(json_file)
            summDict[data['CaseID']] = data['SUMMARY'] # Get Id and Summary of each JSON file.

    return  summDict



summDict = GetSummaryFromJSONFiles()
for key, value in summDict.items():
#    TokenizeParagraph(value)
    # Extract Weatther Features
    extractweatherclimate.dayTimeExtractorSummary(value)
    extractweatherclimate.weatherExtractorSummary(value)

    # Extract Road Features
    extractroadtypedirection.roadDirectionExtractorSummary(value)

    # Extract V1 information
    #https://www.linkedin.com/pulse/triplets-concept-extraction-from-english-sentence-deep-swamynathan

    # Extract V2 information

    # Extract Accident information.

