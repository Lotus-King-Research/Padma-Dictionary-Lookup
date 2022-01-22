import unicodedata as ud

def is_latin(word):
    return all(['LATIN' in ud.name(c) for c in word])