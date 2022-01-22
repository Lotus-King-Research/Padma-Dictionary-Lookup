def modify_input_string(token):

    '''Takes in a token and cleans it up'''
    
    out = ''

    s = token
    
    # clean up start
    if s.startswith('།།'):
        s = s.replace('།།', '')
    if s.startswith('།'):
        s = s.replace('།', '')
    
    # clean up ending
    if s.endswith('།།'):
        s = s.replace('།།', '་')
    if s.endswith('།'):
        s = s.replace('།', '་')
    
    return s