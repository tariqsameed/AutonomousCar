import gensim
import csv

with open('../resources/corpus/weatherandclimate.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    # List of words in each row.
    for row in readCSV:
            print(row)



# Load Google's pre-trained Word2Vec model.
#model = gensim.models.KeyedVectors.load_word2vec_format('../resources/googleword2vec/GoogleNews-vectors-negative300.bin.gz', binary=True)
#model.init_sims(replace=True)

#print(model.most_similar("dry"))

#del model

expandedwords = ['arsal','zohaib','zeeshan']

# File to write data in CSV file.
out_file = open('../resources/corpus/test.csv','w')
line = ""
for item in expandedwords:
    line = line+","+item

out_file.write(line[1:]+"\n")
out_file.close()