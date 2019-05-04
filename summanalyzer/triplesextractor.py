import spacy
import textacy

nlp = spacy.load("en_core_web_sm")
text = nlp(u'	This crash occurred on a two-way, not physically divided roadway, in the middle of a "T" intersection. V1 was traveling west, turning right. The front of V1 contacted the front of V2 as V2 was heading south. V1 had to be towed from the scene, but no occupants were transported. The road conditions at the time of the accident were wet, and it was raining.')
text_ext = textacy.extract.subject_verb_object_triples(text)
print(list(text_ext))

