import tag_natasha, tag_pymorphy, tag_stanza
import logging

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    file_data = {}
    file_data['natasha'] = tag_natasha.process()
    file_data['pymorphy'] = tag_pymorphy.process()
    file_data['stanza'] = tag_stanza.process()

    print(file_data)
