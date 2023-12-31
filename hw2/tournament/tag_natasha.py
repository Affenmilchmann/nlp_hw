from natasha import NewsMorphTagger, NewsEmbedding, Doc, Segmenter
from nltk import tokenize
from pathlib import Path
import xml.etree.ElementTree as ET
import logging

try:
    from . import tag_toolkit
except ImportError:
    import tag_toolkit

logger = logging.getLogger(__name__)

def process(text_file: str = 'text.txt') -> str:
    """Processes input text and returns path to the result file."""
    # Checking if output file alr exists
    output_file = 'parsed_data/natasha.xml'
    if not Path(output_file).is_file():
        output_file = Path(__file__).parent.joinpath(output_file)
    if tag_toolkit.file_exists(output_file, relative_point=__file__):
        return str(Path(output_file).absolute())
    # Reading input file
    text = tag_toolkit.read_file(text_file, relative_point=__file__)
    tokens = tag_toolkit.tokenize_without_punkt(text)
    # Tagging POS
    segmenter = Segmenter()
    morph_tagger = NewsMorphTagger(NewsEmbedding())
    data = ET.Element('data')
    for tkn in tokens:
        doc = Doc(tkn)
        doc.segment(segmenter)
        doc.tag_morph(morph_tagger)

        xml_word = ET.SubElement(data, 'word')
        xml_word.set('word', tkn)
        xml_word.set('pos', doc.tokens[0].pos)
    # Saving results
    tree = ET.ElementTree(data)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding='utf-8')

    return str(output_file.absolute())

if __name__ == '__main__':
    process()
