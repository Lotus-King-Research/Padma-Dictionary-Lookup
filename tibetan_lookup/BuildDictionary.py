class BuildDictionary:

    '''Builds a dictionary with query engine.'''

    def __init__(self, dictionaries=[], debug=False):

        '''
        dictionaries | list | a list of dictionary names as strings

        NOTE: add ability to ingest csv directly
        '''

        import pandas as pd

        self.dictionaries = {}

        if debug is True:

            self.dictionaries['debug_true'] = self._debug_true()

        else:

            self._base_url = 'https://raw.githubusercontent.com/Lotus-King-Research/Padma-Dictionary-Data/v2/data/'

            self.available_dictionaries = pd.read_csv(self._base_url + 'dictionaries.csv')

            # handle the case for custom selection of dictionaries
            if len(dictionaries) > 0:
                _temp = self.available_dictionaries[self.available_dictionaries['Label'].isin(dictionaries)]
                self.available_dictionaries = _temp

            for row in self.available_dictionaries.iterrows():

                filename = row[1]['Name']
                title = row[1]['Title']
                label = row[1]['Label']

                print("Downloading : %s" % title)

                self.dictionaries[label] = pd.read_csv(self._base_url + filename,
                                                       sep='\t',
                                                       header=0,
                                                       names=['Tibetan', 'Description'])

    def _debug_true(self):
        
        import pandas as pd

        df = pd.DataFrame()
        df['Tibetan'] = ['བྱང་ཆུབ་ཀྱི་སེམས་','བྱང་ཆུབ་', 'སེམས་']
        df['Description'] = ['Mind of awakening', 'awakening', 'mind']

        return df

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

    def lookup(self, string, sources=[], partial_match=False):

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
        
        from .utils.check_if_wylie import check_if_wylie

        # transform inputs
        string = check_if_wylie(string).replace(' ', '')

        # init
        if len(sources) == 0:
            sources = list(self.dictionaries.keys())

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
