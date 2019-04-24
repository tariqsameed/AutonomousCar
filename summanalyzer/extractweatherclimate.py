import spacy
import nltk
import csv
import re

nlp = spacy.load("en_core_web_sm")

def getClimateWeatherDictionary():
    climateweatherdictionary = []

    # Get Basic Words List
    with open('../resources/corpus/weatherandclimate.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # List of words in each row.
        for row in readCSV:
            for item in row:
                climateweatherdictionary.append(item)

    # Get Extended Word2Vec List
    with open('../resources/corpus/weatherandclimateword2vec.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # List of words in each row.
        for row in readCSV:
            for item in row:
                climateweatherdictionary.append(item)


    return climateweatherdictionary


# Output is morning, afternoon,evening, midnight etc
def dayTimeExtractorSummary(sentences):
    senten = nlp(sentences)
    for ent in senten.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)


def weatherExtractorSummary(sentences):
    sentenceTokens = nltk.word_tokenize(sentences)
    outofcontextwords = ['low','lower', 'medium','high','higher','moderate','impact']

    climateweatherdictionary = getClimateWeatherDictionary()
    print(len(climateweatherdictionary))
    print(climateweatherdictionary)
    for line in sentenceTokens:
        words = nltk.word_tokenize(line)
        for word in words:
            if word in climateweatherdictionary:
                if len(re.compile('\W').split(word)) < 2 and word in outofcontextwords:
                        # do not add this word
                    outofcontextwords.append(word)
                else:
                    print(word)
