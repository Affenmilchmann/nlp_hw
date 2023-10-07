import stanza
from typing import List, Tuple, Generator

nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos,lemma')

def tokenize_and_tag(text: str) -> List[Tuple[str, str]]:
    '''Tokenizez, tags POS and lemmatizes using stanza pipeline.
    Returns words in tuples (lemma, POS tag)'''
    doc = nlp(text)
    blacklist = ['PUNCT']
    words = [ word for sent in doc.sentences for word in sent.words if not word.upos in blacklist ]
    return [ (word.lemma, word.upos) for word in words ]
