def _get_similarity(a, word):
    
    from strsimpy.jaro_winkler import JaroWinkler
    jarowinkler = JaroWinkler()
    
    sim = jarowinkler.similarity(a, word)
    
    return sim, a

def fuzzy_matching(search_string, lookup_results, n=10, threshold=0.85):
    
    import pandas as pd
    
    words = pd.Series(lookup_results.keys())
    words = words.apply(_get_similarity, args=(search_string,))
    words = pd.DataFrame(words)
    words = words.sort_values(0, ascending=False).head(n)
    words = [i[1] for i in words[0].tolist() if i[0] >= threshold]
    words = pd.DataFrame(words)[0].tolist()
    
    return words