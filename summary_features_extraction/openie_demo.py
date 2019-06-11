#https://stackoverflow.com/questions/32879532/stanford-nlp-for-python
from stanfordcorenlp import StanfordCoreNLP
import json

nlp = StanfordCoreNLP(r'F:\Softwares\stanford-corenlp-full-2018-10-05')

#sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'
#sentence = 'Upon impact V2 rotated clockwise, coming to final rest in the eastbound lane of travel, facing west.' #  V1 rotated clockwise, coming to final rest in southbound lane, facing north

sentence = 'The front of V1 contacted the back of V2.'
sentence = 'V1 front hit V2 in the left side.'

properties = properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                         "outputFormat": "json","openie.triple.strict":"true"}
output = nlp.annotate(sentence, properties=properties)
output =  json.loads(output)
result = [output["sentences"][0]["openie"] for item in output]
for i in result:
     for rel in i:
         relationSent=rel['subject'],rel['relation'],rel['object']
         print(relationSent)