import spacy


nlp = spacy.load("en_core_web_sm")

# Output is morning, afternoon,evening, midnight etc
def dayTimeExtractorSummary(sentences):
    senten = nlp(sentences)
    for ent in senten.ents:
        print(ent.text, ent.start_char, ent.end_char, ent.label_)