#https://stackoverflow.com/questions/32879532/stanford-nlp-for-python
from stanfordcorenlp import StanfordCoreNLP
import json

nlp = StanfordCoreNLP(r'F:\Softwares\stanford-corenlp-full-2018-10-05')

sentence = 'Guangdong University of Foreign Studies is located in Guangzhou.'

properties = properties={"annotators":"tokenize,ssplit,pos,depparse,natlog,openie",
                         "outputFormat": "json","openie.triple.strict":"true"}
output = nlp.annotate(sentence, properties=properties)
output =  json.loads(output)
result = [output["sentences"][0]["openie"] for item in output]
for i in result:
     for rel in i:
         relationSent=rel['subject'],rel['relation'],rel['object']
         print(relationSent)