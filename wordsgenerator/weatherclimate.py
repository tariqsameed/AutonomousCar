import numpy as np
print (np.__version__)

import gensim
import csv
import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

wordlist = []
expandedwords = []
with open('../resources/corpus/weather_corpus/weatherandclimate.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    # List of words in each row.
    for row in readCSV:
            for item in row:
                tokenized_text = nltk.word_tokenize(item)
                for w in tokenized_text:
                    if w not in stop_words:
                        wordlist.append(w)


print(len(wordlist))
# Load Google's pre-trained Word2Vec model.
#model = gensim.models.KeyedVectors.load_word2vec_format('../resources/googleword2vec/GoogleNews-vectors-negative300.bin.gz', binary=True)
#model.init_sims(replace=True)
model = gensim.models.KeyedVectors.load_word2vec_format('/home/sameed/Masters-Passau/GoogleNews-vectors-negative300.bin', binary=True)
model.init_sims(replace=True)

for item in wordlist:
    similarList = model.most_similar(item)
    for item in similarList[:5]:
        expandedwords.append(item[0])

del model

print(len(expandedwords))


# File to write data in CSV file.
out_file = open('../resources/corpus/weather_corpus/weatherandclimateword2vec.csv','w')
line = ""
for item in expandedwords:
    line = line+","+item.encode('utf8').replace("_", " ")

out_file.write(line[1:]+"\n")
out_file.close()