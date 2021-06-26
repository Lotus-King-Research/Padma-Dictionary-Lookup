class BuildDictionary:

    '''Builds a dictionary with query engine.'''

    def __init__(self,
                 mahavyutpatti=True,
                 tony_duff=False,
                 erik_pema_kunsang=False,
                 ives_waldo=False,
                 jeffrey_hopkins=False,
                 lobsang_monlam=False,
                 tibetan_multi=True,
                 tibetan_medicine=False,
                 verb_lexicon=False):

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

    def _download_to_dataframe(self, url):

        '''Helper for downloading the source file to produce dictionary dataframe.'''

        import pandas as pd
        from urllib.request import Request, urlopen

        req = Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
        content = urlopen(req)

        return pd.read_csv(content, index_col=0, error_bad_lines=False)

    def query(self, query, dictionary):

        '''Query dictionaries, regardless if it is already loaded or not.
        
        query | str | the query string
        dictionary | str | name of the dictionary to be used 
        '''

        # see if dictionary is already loaded
        try:
            dictionary = self.dictionaries[dictionary] 
        
        # if not, then load it and keep it
        except KeyError:
            self.dictionaries[dictionary]  = getattr(self, "_" + dictionary)()
            dictionary = self.dictionaries[dictionary]

        out = dictionary[dictionary['Tibetan'] == query]['Description'].tolist()

        if len(out) == 0:
            return None
        else:
            return out

    def partial_match(self, query, dictionary):

        return
