import xml.etree.ElementTree as ET
from typing import List, Tuple
from pathlib import Path
from pprint import pformat
import logging

try:
    from . import tag_natasha, tag_pymorphy, tag_stanza, tag_manual
except ImportError:
    import tag_natasha, tag_pymorphy, tag_stanza, tag_manual

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def load_file(file: str) -> List[Tuple[str, str]]:
    tree = ET.parse(file)
    root = tree.getroot()
    return [(w.attrib['word'], w.attrib['pos']) for w in root.iter('word')]

def main():
    reference_path = tag_manual.output_file
    if not Path(reference_path).is_file():
        reference_path = str(Path(__file__).parent.joinpath(reference_path).absolute())

    # process if not already processed and get paths to the results
    data_paths = {
        'natasha': tag_natasha.process(),
        'pymorphy': tag_pymorphy.process(),
        'stanza': tag_stanza.process()
    }
    logging.info(f"Ready data paths:\n{pformat(data_paths)}")
    # load reference data
    reference_data = load_file(reference_path)
    # calculate accuracy for each
    for name, path in data_paths.items():
        data = load_file(path)
        correct = 0
        for i, (token, pos) in enumerate(reference_data):
            if data[i][0].lower() != token.lower():
                raise ValueError(f"Tokens are not the same between input files. i={i};{data[i][0]}({name})!={token}(reference)")
            correct += int(data[i][1] == pos)
        logger.info(f"Accuracy of {name.upper()}: {correct/len(reference_data):.5f}")


if __name__ == '__main__':
    main()
