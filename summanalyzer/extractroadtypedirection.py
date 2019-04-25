#from nltk.corpus import wordnet as wn
#print(wn.synset('northbound.a.01').hypernyms())

import nltk
import csv
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def getRoadTypeDirectionDictionary():
    roaddtypeirectiondictionary = []

    # Get Basic Words List
    with open('../resources/corpus/road_corpus/roadbasic.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # List of words in each row.
        for row in readCSV:
            for item in row:
                roaddtypeirectiondictionary.append(item)

    # Get Extended Word2Vec List
    with open('../resources/corpus/road_corpus/roadtypedirectionword2vec.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # List of words in each row.
        for row in readCSV:
            for item in row:
                roaddtypeirectiondictionary.append(item)


    return roaddtypeirectiondictionary


# list(set(t))
#https://stackoverflow.com/questions/15547409/how-to-get-rid-of-punctuation-using-nltk-tokenizer

def roadDirectionExtractorSummary(sentences):
    roadkw =[]
    sentenceTokens = nltk.word_tokenize(sentences)
    roaddtypeirectiondictionary = getRoadTypeDirectionDictionary()
    print(len(roaddtypeirectiondictionary))
    for line in sentenceTokens:
        tokenizer = RegexpTokenizer(r'\w+')
        words = tokenizer.tokenize(line)

        for word in words:
            if word in roaddtypeirectiondictionary:
                    print(word)
                    roadkw.append(word)



