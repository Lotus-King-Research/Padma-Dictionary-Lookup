from tibetan_lookup.BuildDictionary import BuildDictionary
tibetan = BuildDictionary(debug_true=True)


def print_tibetan(string,
                  source,
                  return_html=False,
                  debug=False):
    
    from IPython.core.display import HTML
    from botok import Text

    from .modify_input_string import modify_input_string

    string = modify_input_string(string)
    t = Text(string)
    tokens = t.tokenize_words_raw_text.split()
    
    html = '<link rel="stylesheet" href="assets/style.css"><style type="text/css">'
    html += '<style></style>'
    counter = 1

    for i, token in enumerate(tokens):

        token = token.replace('_', ' ')
        original_token = token
        
        try:
            if tokens[i+1].endswith('འི་'):
                token += '་'
        except IndexError:
            pass
            
        if counter % 2 == 0:
            style = 'tibetan-even'
        else:
            style = 'tibetan-odd'
        
        if debug:
            return tibetan.lookup(token)[source]
        
        try:
            text = str(tibetan.lookup(token)[source])
            
            html += '<div class="tooltip-ex ' + style + '"><span>' + original_token + '</span><span class="tooltip-ex-text">' + text  + '</span></div>'
        except (TypeError, KeyError):
            print(token)
            html += '<span class="' + style + '">' + original_token + '</span>'

        counter += 1
        
    html += '<br>'

    display(HTML(html))
    
    if return_html:
        return html