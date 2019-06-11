import re

sentence= 'The car v1 is front hit the back of v2'
verb='hit'

pattern = r'.+?(?='+verb+')'
pre_verb = re.search(pattern, sentence)
print(pre_verb[0].strip())

pattern = r'(?<='+verb+').*'
pre_verb = re.search(pattern, sentence)
print(pre_verb[0].strip())
