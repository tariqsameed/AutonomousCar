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
    # https://pypi.org/project/regex4dummies/
    # https://playwithml.wordpress.com/2016/06/15/extracting-relations-or-subject-predicate-object-triples/
    # https://stackoverflow.com/questions/2705888/rdf-representation-of-sentences/2706567#2706567
    # https://stackoverflow.com/questions/29049974/typed-dependency-parsing-in-nltk-python
    #https://www.analyticsvidhya.com/blog/2019/02/stanfordnlp-nlp-library-python/
    #https://pypi.org/project/stanfordnlp/
    # https://stackoverflow.com/questions/39763091/how-to-extract-subjects-in-a-sentence-and-their-respective-dependent-phrases
    # https://github.com/krzysiekfonal/textpipeliner

    # https://stanfordnlp.github.io/stanfordnlp/

    # Extract V2 information

    # Extract Accident information.

