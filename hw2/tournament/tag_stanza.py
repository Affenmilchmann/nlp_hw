from pathlib import Path
import stanza
import xml.etree.ElementTree as ET
import logging

try:
    from . import tag_toolkit
except ImportError:
    import tag_toolkit

logger = logging.getLogger(__name__)

def process(text_file: str = 'text.txt'):
    """Processes input text and returns path to the result file."""
    # Checking if output file alr exists
    output_file = 'parsed_data/stanza.xml'
    if not Path(output_file).is_file():
        output_file = Path(__file__).parent.joinpath(output_file)
    if tag_toolkit.file_exists(output_file, relative_point=__file__):
        return str(Path(output_file).absolute())
    # Reading input file
    text = tag_toolkit.read_file(text_file, relative_point=__file__)
    tokens = tag_toolkit.tokenize_without_punkt(text)
    # Tagging POS
    nlp = stanza.Pipeline(lang='ru', processors='tokenize,pos')
    data = ET.Element('data')
    for tkn in tokens:
        doc = nlp(tkn)
        xml_word = ET.SubElement(data, 'word')
        xml_word.set('word', tkn)
        xml_word.set('pos', doc.sentences[0].words[0].upos)
            
    tree = ET.ElementTree(data)
    ET.indent(tree, space="\t", level=0)
    tree.write(output_file, encoding='utf-8')

    return str(output_file.absolute())

if __name__ == '__main__':
    process()
