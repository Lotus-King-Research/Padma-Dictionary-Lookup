def dictionary_lookup(request):

    from flask import abort
    from botok import Text
    import tqdm

    from tibetan_lookup import tibetan
    from tibetan_lookup.check_wylie import check_wylie

    # Handle the input query
    search_query = [request.args.get('query')]
    sources = [request.args.get('sources')]

    texts = []

    # Check if input string is wylie or Tibetan
    search_query = check_wylie(str(search_query)).replace(' ', '')

    # In case no sources selected, use Lobsang Monlam
    if len(sources) == 0:
        sources = ['lobsang_monlam']

    t = Text(search_query)
    tokens = t.tokenize_words_raw_text

    for token in tqdm.tqdm(tokens.split()):

        for source in sources:
            sources.append(source)
            try:
                token = token.replace('_', ' ')
                texts.append(tibetan.lookup(token)[5][1][0])
            except (AttributeError, TypeError):
                texts.append[None]
                pass
            
    data = {'search_query': search_query,
            'texts': texts,
            'source': sources, 
            'tokens': tokens}

    return data
