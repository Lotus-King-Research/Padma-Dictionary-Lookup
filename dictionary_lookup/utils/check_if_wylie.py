def check_if_wylie(string):
    
    '''Unless string is Tibetan Unicode, assume it is Wylie and
    perform conversion to Tibetan. 

    string | str | some text

    Example:
    
        check_wylie('thabs')
    '''

    import re
    
    # handle the case where it's Tibetan
    if len(re.findall(r'[\u0f00-\u0fff]+', string)) > 0:
    
        return string
    
    # handle the case where it's Wylie
    else:
    
        string = re.sub(' +', ' ', string)
        string = string.lstrip()
        string = string.rstrip()
        string = string.replace(' ', '་')

        return _wylie_to_tibetan(string)

def _wylie_to_tibetan(wylie_string):
    
    '''Takes in string, and converts to Tibetan following Wylie rules.
    Adds Tsek between syllables and after the last syllable.'''

    import pyewts

    converter = pyewts.pyewts()

    return converter.toUnicode(wylie_string, []) + '་'


