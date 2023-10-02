from natasha import NewsMorphTagger, NewsEmbedding, Doc, Segmenter
import xml.etree.ElementTree as ET
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

output_file = Path('parsed_data/natasha.xml')

def process(text_file: str = 'text.txt'):
    if output_file.is_file():
        logger.info(f"'{output_file}' is present. No pos tagging will be done. Delete this file if you want to redo the tagging")
        return str(output_file.absolute())

    with open(text_file, 'r') as f:
        text = f.read()

    doc = Doc(text)
    segmenter = Segmenter()

    morph_tagger = NewsMorphTagger(NewsEmbedding())
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)

    data = ET.Element('data')
    for word in doc.tokens:
        xml_word = ET.SubElement(data, 'word')
        xml_word.set('word', word.text)
        xml_word.set('pos', word.pos)
            
    tree = ET.ElementTree(data)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding='utf-8')

    return str(output_file.absolute())

if __name__ == '__main__':
    process()
