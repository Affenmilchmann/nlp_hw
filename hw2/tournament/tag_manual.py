import tkinter as tk
from tkinter import messagebox
import xml.etree.ElementTree as ET
from xml.dom import minidom
from nltk import tokenize

output_file = 'parsed_data/manual.xml'

def main():
    pos_tags = [
        "ADJ", "ADP", "ADV", "AUX", "CCONJ",
        "DET", "INTJ", "NOUN", "NUM", "PART",
        "PRON", "PROPN", "PUNCT", "SCONJ", "SYM",
        "VERB", "X"
    ]

    input_file = 'text.txt'
    with open(input_file, 'r') as f:
        text = f.read()

    tokens = list(filter(
        lambda x: x.replace('-','').isalpha(),
        tokenize.word_tokenize(text) 
    ))

    def pretty_print(xml_string):
        parsed_xml = minidom.parseString(xml_string)
        return parsed_xml.toprettyxml(indent="  ")

    class POSTagger:
        def __init__(self, tokens, pos_tags):
            self.window = tk.Tk()
            self.window.title("POS Tagger")
            
            self.tokens = tokens
            self.pos_tags = pos_tags
            self.current_token_index = 0
            self.alr_tagged = {}
            self.tagged_words = []

            self.word_label = tk.Label(self.window, text=self.tokens[self.current_token_index], font=("Helvetica", 16))
            self.word_label.pack()
            self.index_label = tk.Label(self.window, text=f"{self.current_token_index + 1}/{len(self.tokens)}", font=("Helvetica", 16))
            self.index_label.pack()

            for pos_tag in self.pos_tags:
                button = tk.Button(self.window, text=pos_tag, command=lambda pos_tag=pos_tag: self.tag_word(pos_tag))
                button.pack()

            self.save_button = tk.Button(self.window, text="Save", command=self.save)
            self.save_button.pack()

        def tag_word(self, pos_tag):
            self.alr_tagged[self.tokens[self.current_token_index].lower()] = pos_tag
            while self.tokens[self.current_token_index].lower() in self.alr_tagged and self.current_token_index < len(self.tokens):
                self.tagged_words.append((
                    self.tokens[self.current_token_index], 
                    self.alr_tagged[self.tokens[self.current_token_index].lower()]
                ))
                self.current_token_index += 1
            self.index_label.config(text=f"{self.current_token_index + 1}/{len(self.tokens)}")
            if self.current_token_index < len(self.tokens):
                self.word_label.config(text=self.tokens[self.current_token_index])
            else:
                messagebox.showinfo("Information", "All words have been tagged.")

        def save(self):
            root = ET.Element('data')
            for word, pos_tag in self.tagged_words:
                word_element = ET.SubElement(root, 'word')
                word_element.set('word', word)
                word_element.set('pos', pos_tag)
            tree = ET.ElementTree(root)
            ET.indent(tree, space="\t", level=0)
            tree.write(output_file, encoding='utf-8')

        def run(self):
            self.window.mainloop()

    tagger = POSTagger(tokens, pos_tags)
    tagger.run()

if __name__ == '__main__':
    main()