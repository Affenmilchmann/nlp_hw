from pathlib import Path
from nltk import tokenize
from typing import Tuple, Literal
from collections import Counter

from ._tagger import tokenize_and_tag

data_file = Path(__file__).parent.joinpath('data/reviews.json')

def encode_gram_type(token: str, gram_type: Literal['tag', 'lemma']) -> str:
    """Adds prefix 'T_' for pos tags and 'L_' for lemmas
    
    since we are deling with multi class ngrams, 
    here we mark them just in case we will have 'NOUN' token"""
    if gram_type == 'tag': 
        type_letter = 'T'
        token = token.upper()
    elif gram_type == 'lemma': 
        type_letter = 'L'
        token = token.lower()
    else: raise ValueError(f"gram_type must be one of two options. Not {gram_type}")
    return f"{type_letter}_{token}"

def parse_review(review: str) -> Tuple[Counter, Counter]:
    """Returns counts of all bigrams and trigrams in a text.
    Will cover all combinations of POS TAG or lemma.
    
    Example:
    `parse_review('как дела')`
    Will cover all 4 combinations 'L_как + L_дело', 'L_как + T_NOUN', 'T_SCONJ + L_дело' and 'T_SCONJ + T_NOUN'
    
    """
    tokens = tokenize_and_tag(review)
    bigrams_table = Counter()
    trigrams_table = Counter()
    gram_types = {
        0: 'lemma',
        1: 'tag'
    }
    for i in range(len(tokens)):
        # bigrams
        if i + 1 < len(tokens):
            # this loop will cover every combination of lemmas and pos tags
            # from "big(Adj) hat(Noun)" it will generate:
            # "big hat", "big NOUN", "ADJ hat", "ADJ NOUN"
            for j in range(4):
                frst_type = j // 2
                scnd_type = j % 2
                bigram = (
                    encode_gram_type(tokens[i    ][frst_type], gram_types[frst_type]),
                    encode_gram_type(tokens[i + 1][scnd_type], gram_types[scnd_type])
                )
                bigrams_table[' + '.join(bigram)] += 1
        # trigrams
        if i + 2 < len(tokens):
            # Same as with bigrams just for trigrams
            for j in range(8):
                frst_type = j // 4
                scnd_type = (j // 2) % 2
                thrd_type = j % 2
                trigram = (
                    encode_gram_type(tokens[i    ][frst_type], gram_types[frst_type]),
                    encode_gram_type(tokens[i + 1][scnd_type], gram_types[scnd_type]),
                    encode_gram_type(tokens[i + 2][thrd_type], gram_types[thrd_type]),
                )
                trigrams_table[' + '.join(trigram)] += 1
    return (bigrams_table, trigrams_table)
