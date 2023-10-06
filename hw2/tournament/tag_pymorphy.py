from pymorphy2 import MorphAnalyzer
from nltk import tokenize
from pathlib import Path
import xml.etree.ElementTree as ET
import logging

try:
    from . import tag_toolkit
except ImportError:
    import tag_toolkit

logger = logging.getLogger(__name__)

def convert_pos(pos: str) -> str:
    """Converts russian pos used by pymorphy (https://pymorphy2.readthedocs.io/en/stable/user/grammemes.html)
    
    To universal POS tags (https://universaldependencies.org/u/pos/)
    
    What universal POS tags are possible to get
    +ADJ 	+ADP 	-PUNCT
    +ADV 	-AUX 	-SYM
    +INTJ 	+CCONJ 	-X
    +NOUN 	-DET 	 
    -PROPN 	+NUM 	 
    +VERB 	+PART 	 
  	+PRON 	 
  	-SCONJ 	

    """
    lookup_table = {
        'NOUN': 'NOUN',
        'ADJF': 'ADJ',
        'ADJS': 'ADJ',
        'COMP': 'ADJ',
        'VERB': 'VERB',
        'INFN': 'VERB',
        'PRTF': 'ADJ', # NOUN or ADJ idk
        'PRTS': 'VERB', # VERB or ADJ idk
        'GRND': 'VERB',
        'NUMR': 'NUM',
        'ADVB': 'ADV',
        'NPRO': 'PRON',
        'PRED': 'ADV', # ADV or ADJ idk
        'PREP': 'ADP',
        'CONJ': 'CCONJ',
        'PRCL': 'PART',
        'INTJ': 'INTJ',
        '': 'X'
    }
    return lookup_table[pos]

def process(text_file: str = 'text.txt'):
    """Processes input text and returns path to the result file."""
    # Checking if output file alr exists
    output_file = 'parsed_data/pymorphy.xml'
    if not Path(output_file).is_file():
        output_file = Path(__file__).parent.joinpath(output_file)
    if tag_toolkit.file_exists(output_file, relative_point=__file__):
        return str(Path(output_file).absolute())
    # Reading input file
    text = tag_toolkit.read_file(text_file, relative_point=__file__)
    tokens = tag_toolkit.tokenize_without_punkt(text)
    # Tagging POS
    morph = MorphAnalyzer()
    data = ET.Element('data')
    for tkn in tokens:
        pos = morph.parse(tkn)[0].tag.POS
        if not pos: pos = ''
        xml_word = ET.SubElement(data, 'word')
        xml_word.set('word', tkn)
        xml_word.set('pos', convert_pos(pos))
    # Saving results
    tree = ET.ElementTree(data)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding='utf-8')

    return str(output_file.absolute())

if __name__ == '__main__':
    process()
