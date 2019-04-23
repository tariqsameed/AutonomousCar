import json
import glob
import nltk
import extractdaytime

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
    TokenizeParagraph(value)
    extractdaytime.dayTimeExtractorSummary(value)


