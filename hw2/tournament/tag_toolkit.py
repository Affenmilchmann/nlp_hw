from pathlib import Path
from typing import List
from nltk import tokenize

def file_exists(file: str, relative_point: str) -> bool:
    """Checks if `file` exists. Makes two attempts:
    
    1) if `file` exists
    
    2) if join(`relative_point`, `file`) exists
    
    `relative_point` is meant to be __file__ from the caller module."""
    file = Path(file)
    if file.is_file():
        return True
    else:
        relative_output_file = Path(relative_point).parent.joinpath(file)
        if relative_output_file.is_file():
            return True
        else:
            file = relative_output_file

def read_file(file: str, relative_point: str) -> str:
    """Reads data from `file`. Makes two attempts:
    
    1) if `file` exists
    
    2) if join(`relative_point`, `file`) exists
    
    `relative_point` is meant to be __file__ from the caller module."""
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read().lower()
    except FileNotFoundError:
        relative_path = Path(relative_point).parent.joinpath(file)
        with open(relative_path, 'r', encoding='utf-8') as f:
            return f.read().lower()
        
def tokenize_without_punkt(text: str) -> List[str]:
    """Tokenize word and filter punctuation out while keeping
    words like 'как-то'."""
    return list(filter(
        lambda x: x.replace('-','').isalpha(),
        tokenize.word_tokenize(text) 
    ))