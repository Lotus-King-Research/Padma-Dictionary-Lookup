class BuildDictionary:

    '''Builds a dictionary with query engine.'''

    def __init__(self,
                 mahavyutpatti=False,
                 tony_duff=False,
                 erik_pema_kunsang=False,
                 ives_waldo=False,
                 jeffrey_hopkins=False,
                 lobsang_monlam=False,
                 tibetan_multi=False,
                 tibetan_medicine=False,
                 verb_lexicon=False,
                 debug_true=False):

        # build dictionaries based on configuration

        self.dictionaries = {}
        self._base_url = 'https://multi-dictionary-data.padma.io/'

        if mahavyutpatti:
            self.dictionaries['mahavyutpatti'] = self._mahavyutpatti()

        if tony_duff:
            self.dictionaries['tony_duff'] = self._tony_duff()
        
        if erik_pema_kunsang:
            self.dictionaries['erik_pema_kunsang'] = self._erik_pema_kunsang()

        if ives_waldo:
            self.dictionaries['ives_waldo'] = self._ives_waldo()

        if jeffrey_hopkins:
            self.dictionaries['jeffrey_hopkins'] = self._jeffrey_hopkins()

        if lobsang_monlam:
            self.dictionaries['lobsang_monlam'] = self._lobsang_monlam()

        if tibetan_multi:
            self.dictionaries['tibetan_multi'] = self._tibetan_multi()

        if tibetan_medicine:
            self.dictionaries['tibetan_medicine'] = self._tibetan_medicine()

        if verb_lexicon:
            self.dictionaries['tibetan_verbs'] = self._verb_lexicon()

        if debug_true:
            self.dictionaries['debug_true'] = self._debug_true()

    def _mahavyutpatti(self):

        url = 'Mahavyutpatti-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _tony_duff(self):

        url = 'TonyDuff-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _erik_pema_kunsang(self):

        url = 'ErikPemaKunsang-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _ives_waldo(self):

        url = 'IvesWaldo-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _jeffrey_hopkins(self):

        url = 'JeffreyHopkins-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _lobsang_monlam(self):

        url = 'LobsangMonlam-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _tibetan_multi(self):

        url = 'TibetanMulti-Part1-Dictionary.csv'
        temp = self._download_to_dataframe(self._base_url + url)
        url = 'TibetanMulti-Part2-Dictionary.csv'
        temp = temp.append(self._download_to_dataframe(self._base_url + url))
        url = 'TibetanMulti-Part3-Dictionary.csv'
        return temp.append(self._download_to_dataframe(self._base_url + url))

    def _tibetan_medicine(self):

        url = 'TibetanMedicine-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _verb_lexicon(self):
        
        url = 'VerbLexicon-Dictionary.csv'
        return self._download_to_dataframe(self._base_url + url)

    def _debug_true(self):
        
        import pandas as pd

        df = pd.DataFrame()
        df['Tibetan'] = ['བྱང་ཆུབ་ཀྱི་སེམས་','བྱང་ཆུབ་', 'སེམས་']
        df['Description'] = ['Mind of awakening', 'awakening', 'mind']

        return df

    def _download_to_dataframe(self, url):

        import warnings
        
        '''Helper for downloading the source file to produce dictionary dataframe.'''

        import pandas as pd
        from urllib.request import Request, urlopen

        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
        content = urlopen(req)

        warnings.simplefilter('ignore')
        
        return pd.read_csv(content, index_col=0, error_bad_lines=False)

    def _query(self, query, dictionary, partial_match=False):

        '''Helper for querying dictionaries. If the dictionary have not been loaded yet,
        it will automatically be added into the dictionary object (self).
        
        query | str | the query string
        dictionary | str | name of the dictionary to be used 
        partial_match | bool | if partial match should be used
        '''

        # see if dictionary is already loaded
        try:
            dictionary = self.dictionaries[dictionary] 
        
        # if not, then load it and keep it
        except KeyError:
            self.dictionaries[dictionary]  = getattr(self, "_" + dictionary)()
            dictionary = self.dictionaries[dictionary]

        out = {}

        # handle partial match queries
        if partial_match:
            
            tibetan = dictionary[dictionary['Tibetan'].str.contains(query)]['Tibetan'].tolist()
            description = dictionary[dictionary['Tibetan'].str.contains(query)]['Description'].tolist()
           
            for i, word in enumerate(tibetan):
                out[word] = str(description[i])

            if query in list(out.keys()) is False:
                out[query] = None

        # handle exact match queries
        else:
            out[query] = dictionary[dictionary['Tibetan'] == query]['Description'].tolist()

        return out

    def lookup(self, string, sources=['lobsang_monlam'], partial_match=False):

        '''Lookup Tibetan words from one or more dictionaries.
        
        string | str | the Tibetan string to be looked up
        sources | list or None | a list with one or more dictionary names

        Available sources:

        'mahavyutpatti'
        'tony_duff'
        'erik_pema_kunsang'
        'ives_waldo'
        'jeffrey_hopkins'
        'lobsang_monlam'
        'tibetan_multi'
        'tibetan_medicine'
        'verb_lexicon'
        'debug_true' (for debugging only)

        NOTE: `string` must end in tsek.'''
        
        from tibetan_lookup.utils.check_if_wylie import check_if_wylie

        # transform inputs
        string = check_if_wylie(string).replace(' ', '')

        # init
        if isinstance(sources, str):
           sources = [sources]

        out_dict = {}
        
        # handle the lookup
        for source in sources:
            
            out_dict[source] = []
            
            # check for partial match (e.g. 'sems' will also return 'semsnyis').
            if partial_match:
                out_dict[source] = self._query(string, source, partial_match=True)
            
            # exact match
            else:
                out_dict[source] = self._query(string, source)
        
        # return a dictionary where first keys are sources
        # and first keys of first keys are words.
        return out_dict
