# Seprate sentennces and paragraph into Precrash Event, Impact and Pos Crah Event.
# Iterate the sentences get the sentences based on feature vector.


# Things to do
# Put all lines in pre crash until crash event is detected. , extract road geometry, direction.
# On crash. 1) Extract the location of impact, point of impact:  Enable post crash event.
# https://medium.com/factory-mind/regex-tutorial-a-simple-cheatsheet-by-examples-649dc1c3f285
# In post crash event, detect rotation (spinning, clockwise, counter-clockwise) and direction., distance



import glob
import json
import os
import nltk
from nltk.tokenize import RegexpTokenizer
import nltk.tokenize as tokenize
from stanfordcorenlp import StanfordCoreNLP
import json
import re

import sys
sys.stdout = open('crash_event_impact.txt','w')

nlp = StanfordCoreNLP(r'F:\Softwares\stanford-corenlp-full-2018-10-05')



pre_crash_counter = 0
crash_counter = 0
pro_crash_counter = 0




def pre_crash_event(summary):
    print(summary)

def crash_event(summary):
    global crash_counter
    crash_event_sentences = []
    sentenceTokens = tokenize.sent_tokenize(summary)
    for line in sentenceTokens:
        line = line.strip()  #\r\n , remove these from lines.

        list_ = ['impact','struck', 'hit', 'contacted','impacted'] # Create Google Word 2 Vector list to increase accuracy
        if any(word in line for word in list_):
            print(line)
            crash_event_sentences.append(line)
            crash_counter = crash_counter + 1

    # V1 Impact area, V2 impact area
    # Start Analysis of Specific Sentences.

    for impact_sentence in crash_event_sentences:
        properties = {"annotators": "tokenize,ssplit,pos,depparse,natlog,openie",
                      "outputFormat": "json", "openie.triple.strict": "true"}

        output = nlp.annotate(impact_sentence, properties=properties)
        output = json.loads(output)
        result = [output["sentences"][0]["openie"] for item in output]
        for i in result:
            for rel in i:
                relationSent = rel['subject'], rel['relation'], rel['object']
                print(relationSent)

                if any(word in rel['relation'] for word in list_):
                    print(rel['relation'])

                    # case 1: subject and object contain car part location.
                    if (rel['subject'] in [ 'front','rear', 'back', 'right', 'left', 'right side', 'left side']) and (rel['object'] in [ 'front','rear', 'back', 'right', 'left', 'right side', 'left side']):
                        print("Case 1")

                        # case 2: subject is car and object contain car part location of seconde car.
                    elif (rel['subject'] in ['vehicle', 'Vehicle', 'v1', 'V1', 'v2', 'V2']) and (rel['object'] in ['front', 'rear', 'back', 'right', 'left', 'right side', 'left side']):
                            print("Case 2")

                        # default case: (car,part location) , verb, (car,part location)
                        # rear end, head on, angle/side , left, right
                    else:
                        print("default case")
                        for word in list_:
                            if word in rel['relation']:
                                verb = word
                                pattern = r'.+?(?='+verb+')'
                                pre_verb = re.search(pattern, impact_sentence)
                                print(pre_verb[0])

                                pattern = r'(?<='+verb+').*'
                                pre_verb = re.search(pattern, impact_sentence)
                                print(pre_verb[0].strip())


def post_crash_event(summary):
    sentenceTokens =  tokenize.sent_tokenize(summary)
    for line in sentenceTokens:
         if "impact" in line:
            print(line)


entries = os.listdir('../resources/summary/')
for file in entries:
    jsonFile = glob.glob("../resources/summary/"+file)
    summDict = {}
    print(jsonFile[0])
    with open(jsonFile[0], 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        summDict[data['CaseID']] = data['SUMMARY'] # Get Id and Summary of each JSON file.
        #pre_crash_event(data['SUMMARY'])
        crash_event(data['SUMMARY'])
        #post_crash_event(data['SUMMARY'])


print(crash_counter)