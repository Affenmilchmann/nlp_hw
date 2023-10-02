import stanza
import xml.etree.ElementTree as ET
from nltk import tokenize
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

output_file = Path('parsed_data/stanza.xml')

def process(text_file: str = 'text.txt'):
    if output_file.is_file():
        logger.info(f"'{output_file}' is present. No pos tagging will be done. Delete this file if you want to redo the tagging")
        return str(output_file.absolute())
    
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos')
    with open(text_file, 'r') as f:
        text = f.read()
    doc = nlp(text)

    data = ET.Element('data')
    for sent in doc.sentences:
        for word in sent.words:
            xml_word = ET.SubElement(data, 'word')
            xml_word.set('word', word.text)
            xml_word.set('pos', word.upos)
            
    tree = ET.ElementTree(data)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding='utf-8')

    return str(output_file.absolute())

if __name__ == '__main__':
    process()
