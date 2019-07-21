import re
from nltk.tokenize import word_tokenize

# sentence= 'The car v1 is front hit the back of v2'
# verb='hit'
#
# pattern = r'.+?(?='+verb+')'
# pre_verb = re.search(pattern, sentence)
# print(pre_verb[0].strip())
#
# pattern = r'(?<='+verb+').*'
# pre_verb = re.search(pattern, sentence)
# print(pre_verb[0].strip())
#
#
# import re
# x="This three Vehicle crash occurred in the middle of a four-way intersection, which was controlled by traffic signals in all directions"
# print(re.sub(r"\bthree vehicle\b","V1" ,x, re.IGNORECASE))
#
# print(x.replace("three Vehicle", "V3"))


# import csv
#
# row = ['2', ' Marie', ' California']
#
# with open('people.csv', 'r') as readFile:
#     reader = csv.reader(readFile)
#     lines = list(reader)
#     lines[2] = row
#
# with open('people.csv', 'w') as writeFile:
#     writer = csv.writer(writeFile)
#     writer.writerows(lines)
#
# readFile.close()
# writeFile.close()

# text = 'V1 continued off the roadway, made contact with its front plane to a tree, rotated counter'
# word_tokens = word_tokenize(text)
# print(word_tokens)

# sentence = 'came to rest.'
# verb = 'rest'
# pattern = r'(?<='+verb+').*'
# pos_verb = re.search(pattern, sentence)
# print(pos_verb[0].strip())

import csv
csv_columns = ['No','Name','Country']
dict_data = [
{'No': 1, 'Name': 'Alex', 'Country': 'India'},
{'No': 2, 'Name': 'Ben', 'Country': 'USA'},
{'No': 3, 'Name': 'Shri Ram', 'Country': 'India'},
{'No': 4, 'Name': 'Smith', 'Country': 'USA'},
{'No': 5, 'Name': 'Yuva Raj', 'Country': 'India'},
]
csv_file = "test.csv"
try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
        writer.writeheader()
        for data in dict_data:
            writer.writerow(data)
except IOError:
    print("I/O error")