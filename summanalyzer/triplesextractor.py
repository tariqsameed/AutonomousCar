import spacy
import textacy
import requests

def gettriplespacy(text):
    nlp = spacy.load("en_core_web_sm")
    text = nlp(text)
    text_ext = textacy.extract.subject_verb_object_triples(text)
    print(list(text_ext))


def gettripleopie(sentext):
    payload = {'text': sentext}
    r = requests.get("http://localhost:8080/opie", params=payload)
    resp = r.text
    if resp['length'] > 0:
    for val in enumerate(resp['spoList']):
        print(val[1]['subject'],val[1]['predicate'],val[1]['object'])